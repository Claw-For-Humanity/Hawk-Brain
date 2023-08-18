# implement location detection and json
import math
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk
import threading
import numpy as np
import os
import json
import os
import cv2
import logging
import tkinter as tk
import threading
import time
logging.disable(logging.WARNING)

import matplotlib
matplotlib.use('GTK4Agg')

import matplotlib.pyplot as plt
import numpy as np
from six import BytesIO
from PIL import Image
from six.moves.urllib.request import urlopen
from official.vision.ops.preprocess_ops import normalize_image

# from official.vision.detection.ops.postprocess_ops import normalize_image
# import official.vision.detection.ops.postprocess_ops as ops

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.utils import ops as utils_ops
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Hawk_Brain:
    thread1 = None
    thread2 = None
    thread3 = None
    thread4 = None
    thread6 = None
    decodedData = None
    threadKill = threading.Event()
    camLock = threading.Lock()
    detectionLock = threading.Lock()
    cam = None
    std = None
    selectedColour = None
    img = None
    imgtk = None
    tkmg = None
    incomingState = False
    stateKill = threading.Event()
    checkStateLock = threading.Lock()
    receiveLock = threading.Lock()
    state = None
    cam_lock = threading.Lock()
    std = None
    killFlag = threading.Event()
    selectedColour= {'red': False, 'blue' : False}
    redOpt = None
    BluOpt = None
    objBlue = None
    objRed = None
    objectRed = None
    objectBlue = None
    readyDetection = False
    ptBlue = None
    ptRed = None
    distanceLock = threading.Lock()
    boxCheckStat = False
    centerObj = None

    objectX = None
    objectW = None
    slider1 = None
    slider0 = None
    savingData = {}
    savePath = os.getcwd() + "/Hawk-Brain/json"

    # json data
    comList_val = None 
    camList_val = None
    baud_val = None
    slider0Obj = None
    slider1Obj = None
    width = None
    height = None

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    else:
        print('else entered')
        if os.path.exists(os.path.join(savePath, "save.json")):
            print('\n\nLine75 save path exists\n\n')
            f = open(os.path.join(savePath, "save.json"))
            prevData = json.load(f)
            comList_val = prevData['comList_val']
            camList_val = prevData['camList_val']
            baud_val = prevData['baud_val']
            objectX = prevData['slider0Obj']
            objectW = prevData['slider1Obj']
            width = prevData['width']
            height = prevData['height']
        


    def __initiate__(): # returns camport, comport and baudrate
        # create variables
        global window, comList_val, baud_val, camList_val
        baudRates = [300,1200,2400,9600,10417,19200,57600,115200]
        defaultLocX = 30 # default x location 
        defaultLocY = 150
        defaultLocExpl = 130
        # create window using tkinter
        window = tk.Tk()
        window.title("Project Claw For Humanity Port Selector")
        window.geometry("600x240")
        window.resizable(False,False)
        mphoto = PhotoImage(file=f'{os.path.join(os.getcwd(),"sources","cfhmain.png")}')
        window.iconphoto(True, mphoto)
        print (f'\n\n{comList_val}')
        if comList_val != 'None':
            comList_val = tk.StringVar(window, str(comList_val))
        
        else:
            print('comlist val is none')
            comList_val = tk.StringVar(window, "Com Port")
        ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
        ComLable.place(x=defaultLocX,y=20)
        
        if baud_val != 'None':
            baud_val = tk.StringVar(window, str(baud_val))
        else:
            baud_val = tk.StringVar(window, "Baud Rate")
        baudLable = tk.Label(window, text="Select Baud Rate", font=('Arial', 15))  
        baudLable.place(x= defaultLocX, y= 80)
        if camList_val != 'None':
            camList_val = tk.StringVar(window, str(camList_val))
        else:
            camList_val = tk.StringVar(window, "Cam Port")
        
        CamPortLabel = tk.Label(window, text='Select Camera Port', font=('Arial',15))
        CamPortLabel.place(x=defaultLocX, y=defaultLocExpl)
        
        def searchPortCam():
            index = 0
            arr = []
            while True:
                cap = cv2.VideoCapture(index)
                if not cap.read()[0]:
                    break
                else:
                    arr.append(str(f'{index}'))
                cap.release()
                index += 1
            return arr
        
        def searchSerialPort():
            HWID = []
            SerialDescription = []
            i=0
            ports = list(serial.tools.list_ports.comports())
            
            if len(ports) == 0:
                SerialDescription.append("No Ports Available")
                tk.messagebox.showinfo(title = 'warning', message = 'No Ports available')
                exit()
            else:
                while i<len(ports):
                    port = ports[i]
                    HWID.append(port.device)
                    SerialDescription.append(f"Name: {port.device} || Description: {port.description}")
                    i+=1
                    
            return SerialDescription, HWID
        
        def receiveVal():
            print('entered receiveVal')
            
            global HWID, serialDescription
            serialDescription, HWID = searchSerialPort()
            camPorts = searchPortCam()
            
                
            camPorts = searchPortCam()
            ComOption = tk.OptionMenu(window, comList_val, *serialDescription)
            baudOption = tk.OptionMenu(window, baud_val, *baudRates)
            CamOption = tk.OptionMenu(window, camList_val, *camPorts)
            
            ComOption.place(x= defaultLocX, y= 45)
            baudOption.place(x= defaultLocX, y= 100)
            CamOption.place(x=defaultLocX, y= defaultLocY)
                
            window.after(5000, receiveVal)

        
        receiveVal()
        btn = tk.Button(window, text='Next', command=lambda: Hawk_Brain.camera_Setting(camList_val.get(), comList_val.get(),baud_val.get()))
        btn.place(x= defaultLocX+10, y= 200)
        
        window.mainloop()
            
    def camera_Setting(camPort, selectedSerialDescription, bdrate): # accepts camport and globalize captured cam
        
        i = 0
        while i < len(serialDescription):
            if serialDescription[i] != selectedSerialDescription:
                i +=1
            else:
                comPort = HWID[i]
                break
        
        communication = comPort,bdrate
        window.destroy()
        
            # globalize cam // capture cam 
        global cam
        cam = cv2.VideoCapture(int(camPort))

        if cam.isOpened():
            print('camera captured successfully \n')
        else:
            tk.messagebox.showinfo(title= 'warninig', message = 'camera encountered problem // line 165 // unknown issue // exitting')
            Hawk_Brain.camera_Setting(int(camPort), comPort, bdrate)
        
        # create window
        global camWindow,alta
        camWindow = tk.Tk()
        camWindow.title("Camera Setting")
        camWindow.option_add("*Font","Ariel 15")
        camWindow.geometry("500x130")
        camWindow.resizable(True, True)
        
        # entry
        subTitle = tk.Label(camWindow, text='Width x Height for camera')
        subTitle.place(x=30, y=5)
        width = tk.Entry(camWindow, width=4)
        width.place(x=30, y=30)
        
        height = tk.Entry(camWindow, width=4)
        height.place(x=90,y=30)
        
        if width != 'None':
            width.insert(0,Hawk_Brain.prevData["width"])
        else:
            pass
            
        if height != 'None':
            height.insert(0,Hawk_Brain.prevData["height"])
        else:
            pass
        
        x = tk.Label(camWindow, text='X')
        x.place(x=79, y=33)
        
        alta = 0
        def adjust_resolution(width, height, communication): 
            global alta
            if alta == 0:
                alta += 1
                return
            else:
                pass
            print('entered adjust resolution')
            
            Hawk_Brain.camDisplayer(width, height, communication)
            
        
        recommend = tk.Label(camWindow, text=f'recommended camera resolution is {int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))}')
        recommend.place(x= 113, y= 79)
        
        btn = tk.Button(camWindow, text='search', command=lambda: adjust_resolution(int(width.get()), int(height.get()), communication))
        btn.place(x= 150, y= 30)
        
        camWindow.mainloop()
    thread1int = 0
    def threadVid():
        global thread1int,thread1
        print('thread entered')
        def update():
            global std 
            while not Hawk_Brain.killFlag.is_set():
                ret, frame = cam.read()
                with Hawk_Brain.cam_lock:
                    global std
                    if ret:
                        std = frame.copy()
        thread1 = threading.Thread(target=update)
        print('thread defined')
        if thread1int == 0:
            thread1.start()
            thread1int += 1
        print('thread started')
        print(f'thread state is {thread1.is_alive}')

    comCallInt = 0

    def camDisplayer(resolutionX, resolutionY, communication):
        global width, height,comCallInt
        width = resolutionX
        height = resolutionY
        
        
        if not resolutionX and resolutionY:
            resolutionX = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            resolutionY = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            tk.messagebox.showinfo(title = 'warning', message = f'resolution box empty, resolution is automatically set to {resolutionX}x{resolutionY}')
        else:
            if resolutionX == '' or resolutionY == '':
                tk.messagebox.showinfo(title = 'warning', message = 'one of the resolution box is empty // Try it again')
                return
            else:
                cam.set(cv2.CAP_PROP_FRAME_WIDTH, resolutionX)
                cam.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutionY)

        if resolutionX > 1000 or resolutionY > 1000:
            displayResX = int(resolutionX) / 2
            displayResY = int(resolutionY) / 2
        else:
            displayResX = resolutionX
            displayResY = resolutionY
        
        camWindow.geometry(f"{resolutionX + 400 }x{resolutionY + 400}")
        print('about to start thread')
        Hawk_Brain.threadVid()
        print('successfully initiated thread')
        canvas = tk.Canvas(camWindow, width=displayResX, height=displayResY)
        canvas.place(x=30,y=60)
        
        canvas_image = canvas.create_image(0, 50, anchor=tk.NW)
        print('canvas created')
        comCall = tk.Button(camWindow, text='next', command=lambda: Hawk_Brain.__initCom__(communication))    
        

        # update the video in a loop
        def update_canvas():
            global comCallInt
            with Hawk_Brain.cam_lock:
                if type(std) != type(None):
                    pic = std.copy()
                else:
                    print('error / std is none') 
                    return
                    
            frame = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (int(displayResX),int(displayResY)))
                
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            canvas.itemconfig(canvas_image, image = imgtk)
            canvas.image = imgtk
            
            if comCallInt == 0:
                comCall.place(x= 250, y= 30)
                comCallInt += 1
            else:
                pass
            
            camWindow.after(10,update_canvas)
            
        update_canvas()
        
        

    def __initCom__(communication):
        global camWindow,state,comWindow
        
        state = 'checking connection'
        camWindow.destroy()

        comWindow = tk.Tk()
        comWindow.title("ComPort checker")
        comWindow.option_add("*Font","Ariel 15")
        comWindow.geometry("1000x500")
        comWindow.resizable(False, False)

        portInfo = tk.Label(comWindow, text=f'comport connection check // selected comport is {communication[0]} // selected baud rate is {communication[1]}')
        portInfo.place(x=30, y=15)
        
        cntBtn = tk.Button(comWindow, text= 'Connect', command=lambda: Hawk_Brain.logOpen(communication))
        cntBtn.place(x= 30, y= 90)
        comWindow.mainloop()
        
    def log(widget, message, level = 'INFO'):
        tag = level.upper()
        widget.insert(tk.END, message + "\n", tag)

    def send(data):
        global serialInst, sent
        data = str(data)
        sent = data
        print(f'\n{data.encode()} is written\n')
        serialInst.write(f"{data}".encode())    

    def receive(serialInst):
        while not Hawk_Brain.killFlag.is_set():
            if type(serialInst) != type(None):
                if serialInst.in_waiting > 0:
                    decoded = serialInst.readline().decode().strip() # Read data from the serial port
                    with Hawk_Brain.receiveLock:
                        global decodedData, incomingState
                        if decoded != None:
                            incomingState = True
                            decodedData = decoded
                        else:
                            incomingState = False
                            decodedData = None
                            
    def update_gui():
        with Hawk_Brain.receiveLock:
            global decodedData, incomingState, loggingbox
            if incomingState == True:
                Hawk_Brain.log(text_widget, f'incoming bytes from arduino {decodedData}')
                
            elif incomingState == False: 
                Hawk_Brain.log(text_widget, f'waiting for incoming bytes from arduino')

            # check incoming data every second
            loggingbox.after(1000, Hawk_Brain.update_gui) 

    def logOpen(communication):
        
        comWindow.destroy()
        global serialInst, text_widget,loggingbox,thread2
        print('about to start thread 2')
        serialInst = serial.Serial(port=str(communication[0]),baudrate= int(communication[1]))
        thread2 = threading.Thread(target=Hawk_Brain.receive, args=(serialInst,))
        thread2.start()
        
        print(f'thread 2 is started state is : {thread2.is_alive()}')
        
        
        loggingbox = tk.Tk()
        loggingbox.title('logging box')   
        
        with Hawk_Brain.receiveLock:
            if decodedData == None:
                print('check arduino')
                nxt_btn = tk.Button(loggingbox, text="next", command=lambda: Hawk_Brain.colourInterface())
                nxt_btn.place(x=70, y=90)
            else:
                pass
                
        

        loggingbox.geometry("1000x1000")
        loggingbox.resizable(True,True)
        text_widget = tk.Text(loggingbox, height=20, width=80)
        text_widget.pack()
        enter_widget = tk.Entry(loggingbox, width= 18)
        snd_btn = tk.Button(loggingbox, text='send', command=lambda: Hawk_Brain.send(str(enter_widget.get())), width= 2)
        snd_btn.place(x=20, y= 90)
        enter_widget.pack()
        
        Hawk_Brain.log(text_widget, "communication established and waiting for response")

        
        Hawk_Brain.log(text_widget, f"thread called and thread state is {thread2.is_alive}")
            
        loggingbox.after(10, Hawk_Brain.update_gui)
    
    def send_safety(data):
        global serialInst, sent
        sent = str(data)
        data = str(data)
        print(f'\n{data.encode()} is written\n')
        serialInst.write(f"{data}".encode())
        time.sleep(4)
        
    def distanceCalc(colour, ColourCenter):
        print(f'\ncolour: {str(colour)} // value : {ColourCenter}\n')
        while type(centerObj) == type(None):
            print('warning : waiting for centerOBJ to be created')
        
        if not type(ColourCenter) == type(None):
            print('check center value')

            x1 = centerObj[0]
            y1 = centerObj[1]
            
            x = ColourCenter[0]
            y = ColourCenter[1]
            
            distance = np.sign(x1 - x) * math.sqrt((x1 - x)**2 + (y1-y)**2)
        else:
            distance = None
        return distance

    def _detection_():
        global red_lower_colour, red_upper_colour, blue_lower_colour, blue_upper_colour, thread4, readyDetection,centerObj
        red_lower_colour = np.array([162,100,100])
        red_upper_colour = np.array([185,255,255])
        
        blue_lower_colour = np.array([104,50,100])
        blue_upper_colour = np.array([126,255,255])
        
        def resetblu():
            with Hawk_Brain.detectionLock:
                global ptBlue
                ptBlue = None
        
        def resetRed():
            with Hawk_Brain.detectionLock:
                global ptRed
                ptRed = None
        
        # start thread for boxcheck
        thread4 = threading.Thread(target= Hawk_Brain.boxCheck)
        thread4.start()
        
        while not Hawk_Brain.threadKill.is_set():
            def lineColour(distance):
                if distance != None:
                    if distance >= 0: # blue
                        return (0,0,255)
                    elif distance < 0:
                        return(0,255,0) # red
                else:
                    pass
                
            def calcLineCenter(point1, point2):
                center = (int((point1[0] + point2[0])/2),int((point2[1] + point2[1])/2 + 10))
                return center
                
            with Hawk_Brain.camLock:
                video = std
            global result
            bottomHsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
            
            bottom_red_mask = cv2.inRange(bottomHsv, red_lower_colour, red_upper_colour)
            bottom_blue_mask = cv2.inRange(bottomHsv, blue_lower_colour, blue_upper_colour)
            combinedMask = cv2.bitwise_or(bottom_red_mask, bottom_blue_mask)
            result = cv2.bitwise_and(video, video)
            videos = [result, combinedMask]
            contourRed, _1 = cv2.findContours(bottom_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contourRed:
                red = cv2.boundingRect(contour)
                # x,y,w,h
                if red[2]>90 and red[3]>90:          
                    centerred = (2*red[0]+red[2])//2, (2*red[1]+red[3])//2
                    for redVid in videos:
                        if selectedColour['red'] == True:
                            cv2.rectangle(redVid,(red[0],red[1]),(red[0]+red[2],red[1]+red[3]),(172,0,179),2)
                            cv2.circle(redVid, centerred, 1, (255,0,0) ,thickness=3)
                            with Hawk_Brain.detectionLock:
                                global ptRed
                                ptRed = centerred
                                
                                # d = math.sqrt(())
                                # ptRed = ((rx+rw)/2,(ry+rh)/2)
                        else:
                            resetRed()
            
            
            contourBlu, _2 = cv2.findContours(bottom_blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contourBlu:
                blu = cv2.boundingRect(contour)
                if blu[2]>90 and blu[3]>90:          
                    centerBlu = (2*blu[0]+blu[2])//2, (2*blu[1]+blu[3])//2
                    for bluVid in videos:
                        if selectedColour['blue'] == True:
                            cv2.rectangle(bluVid,(blu[0],blu[1]),(red[0]+blu[2],blu[1]+blu[3]),(172,0,179),2)
                            cv2.circle(bluVid, centerBlu, 1, (255,0,0) ,thickness=3)
                            with Hawk_Brain.detectionLock:
                                global ptBlue
                                ptBlue = centerBlu
                                # ptBlue = (int((bx+bw)/2), int((by+bh)/2))
                        else:
                            resetblu()
                
            readyDetection = True
            
            centerObj = int(objectX+ (0.5 * objectW)),int(objectY + (0.5 * objectH))
            
            with Hawk_Brain.distanceLock:
                if boxCheckStat == True:
                    dR = Hawk_Brain.distanceCalc("red", ptRed)
                    dB = Hawk_Brain.distanceCalc("blue",ptBlue)
                    
                else:
                    dR = None
                    dB = None
            
            
            if (type(ptBlue) != type(None)) and (type(None) != type(dB)):
                cv2.line(result, centerObj, ptBlue, lineColour(dB),2)
                print(f"calclinecenter is {calcLineCenter(ptBlue, centerObj)}")
                cv2.putText(result, f"B/{dB}", (calcLineCenter(ptBlue, centerObj)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            else:
                pass
            
            if type(ptRed) != type(None):
                cv2.line(result, ptRed, centerObj, lineColour(dR), 2)
                cv2.putText(result, f"R/{dR}", calcLineCenter(ptRed, centerObj), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            else:
                pass
            
            for boxes in videos:
                cv2.rectangle(boxes, (590,410), (690,310), 2)
            
            # create slider for this later on
            cv2.rectangle(result, (objectX,objectY), (objectX+objectW,objectY+objectH),(0,255,0),3)
            # circle on the center of the target object
            cv2.circle(result, centerObj, 1, (255,0,0) ,thickness=5)
            
            frame = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            with Hawk_Brain.detectionLock:
                global vidResult, img
                vidResult = result
                img = Image.fromarray(frame)

    def boxCheck():
        global objectY, objectH, objectPts, distance
        if objectX == None or objectW == None:
            print('error object X and object W')
            exit()
        objectY = 0
        objectH = 720 
        
        objectPts = np.array([(objectX,objectY),(objectX+objectW, objectY),(objectX+objectW,objectY+objectH),(objectX,objectY+objectH)])
        
        # write command based on arduino
        push_object = 3
        pull_object = 4
        while readyDetection == False:
            print('boxCheck waiting for __detection__')
        
        while not Hawk_Brain.threadKill.is_set():
            with Hawk_Brain.detectionLock:
                global ptBlue
                objectBlue = ptBlue
                objectRed = ptRed

            with Hawk_Brain.distanceLock:
                global boxCheckStat, distanceBlu, distanceRed
                boxCheckStat = True
                distanceBlu = Hawk_Brain.distanceCalc("blue",ptBlue)
                distanceRed = Hawk_Brain.distanceCalc("red",ptRed)
                Widther = widthDis
            
            print(f'objectblue is {ptBlue}')
            
            if type(objectBlue) != type(None):
                if abs(distanceBlu) <= abs(Widther):
                    print('\n\n blue point polygon test less than 0: = ')
                    print(f'distance between blue and object is{distanceBlu}')
                    
                    Hawk_Brain.send_safety(push_object)    
                    Hawk_Brain.log(text_widget, 'line 609')
                
                else:
                    Hawk_Brain.end_safety(pull_object)
                    Hawk_Brain.log(text_widget, 'line 613')
            
            else:
                Hawk_Brain.send_safety(pull_object)
                Hawk_Brain.log(text_widget, 'line 617')
            
            if type(objectRed) != type(None):
                if abs(distanceRed) <= abs(Widther):
                    print('\n\n red point polygon test less than 0: = ')
                    print(f'distance between red and object is{distanceRed}')
                    Hawk_Brain.send_safety(push_object)
                    
                
                else:
                    Hawk_Brain.send_safety(pull_object)
            else:
                Hawk_Brain.send_safety(pull_object)

    def detectionInit():
        global thread6
        resolutionX = 1280
        resolutionY = 720
        displayWindow = tk.Toplevel()
        displayWindow.title("Detection Engine 1.0")
        displayWindow.geometry("2000x1000")
        displayWindow.resizable(True,True)
        canvas = tk.Canvas(displayWindow, width= resolutionX, height=resolutionY)
        canvas.pack()
        canvas_image = canvas.create_image(0,50,anchor = tk.NW)
        
        print('detection initialized')
        
        thread6 = threading.Thread(target=Hawk_Brain._detection_)
        thread6.start()
        
        def updateCanvas():
            print('entered updatecanvas')
            if Hawk_Brain.threadKill.is_set():
                displayWindow.destroy()
                return
            with Hawk_Brain.detectionLock:
                global imgtk
                if img != None:
                    imgtk = ImageTk.PhotoImage(image=img)
                    
                    canvas.itemconfig(canvas_image, image= imgtk) 
                    canvas.image= imgtk
                    
            displayWindow.after(10,updateCanvas)
        
        updateCanvas()
        displayWindow.mainloop()
        
    def colourInterface():
        global redOpt, BluOpt
        # create window for colourselection
        colourWindow = tk.Tk()
        colourWindow.title ('Colour Selection')
        colourWindow.geometry('300x300')
        colourWindow.resizable(True,True)
        
        colourSelectInfo = tk.Label(colourWindow, text=f'Please Select Colour')
        colourSelectInfo.place(x=30, y=15)
            
        redOpt = tk.BooleanVar()
        BluOpt = tk.BooleanVar()
        
        Hawk_Eye_Activate = tk.BooleanVar()
        
        slider0Obj = tk.IntVar() # width
        slider1Obj = tk.IntVar() # x value
        slider2Obj = tk.IntVar() # command sending distance
        
        print(f'redOpt state is {redOpt.get()}')
        print(f'BluOpt state is {BluOpt.get()}')
        
        def updateRedColour():
            global redOpt,selectedColour
            if redOpt.get() == True:
                redOpt.set(False)
            else:     
                redOpt.set(True)
            selectedColour['red'] = redOpt.get()

        def updateBlueColour():
            global BluOpt,selectedColour
            if BluOpt.get() == True:
                BluOpt.set(False)
            else:
                BluOpt.set(True)
            selectedColour['blue'] = BluOpt.get()

        def updateScale():
            global objectX,objectW, objectCS
            objectW = int(slider1.get())
            print(f'ObjectX is {objectX}\n')
            objectX = int(slider0.get())
            print(f'ObjectW is {objectW}\n')
            objectCS = int(slider2.get())
            print(f'objectCS is {objectCS}')
            with Hawk_Brain.distanceLock:
                global widthDis
                widthDis = objectW
        
        def update_HawkEye():
            print('activating Hawk Eye')
            
            # add additional code that activates the hawk eyes
        
        slider0Info = tk.Label(colourWindow, text=f'width')
        slider0Info.place(x=30, y=240)
        
        slider1Info = tk.Label(colourWindow, text=f'X value')
        slider1Info.place(x=30, y=153)
        
        slider2Info = tk.Label(colourWindow, text=f'command sending distance')
        slider2Info.place(x=30, y=213)
        
        # slider 0 - x value
        slider0 = tk.Scale(colourWindow,variable=slider0Obj, orient= HORIZONTAL, from_=0, to=1280, command= updateScale)
        if objectX != 'None':
            slider0.set(int(objectX))
        else:
            slider0.set(200)
        slider0.place(x = 30, y= 230)
        
        # slider 1 - width
        slider1 = tk.Scale(colourWindow,variable=slider1Obj, orient= HORIZONTAL, from_=0, to=1270, command= updateScale)
        if objectW != 'None':
            slider1.set(int(objectW))
        else:
            slider1.set(900)
        slider1.place(x = 30, y= 175)
        
        # slider 2 - command sending distance
        slider2 = tk.Scale(colourWindow, variable=slider2Obj, orient= HORIZONTAL, from_= 0, to= 700, command= updateScale)
        slider2.place(x= 30, y= 285)
        
        
        updateBtn = tk.Checkbutton(colourWindow, text='update', command=lambda: updateScale())
        updateBtn.place(x= 30, y= 300)
        redBtn = tk.Checkbutton(colourWindow, text='red', variable=(redOpt), command= lambda: updateRedColour())
        BlueBtn = tk.Checkbutton(colourWindow, text='blue',variable=(BluOpt), command= lambda: updateBlueColour())
        Hawk_Eye_Activate_Button = tk.Button(colourWindow, text= 'Hawk Eye Activate', command= lambda: update_HawkEye())

        redBtn.place(x=30, y= 45)
        BlueBtn.place(x=130, y= 45)
        Hawk_Eye_Activate_Button.place(x= 155, y= 45)
        
        while type(std) == type(None):
            print('waiting for cam')
        
        nxtBtn = tk.Button(colourWindow, text='next', command=lambda: Hawk_Brain.detectionInit())
        nxtBtn.place(x= 160, y=400)
        
        updateScale()
        colourWindow.mainloop()

    def createJson():
        global savingData
        savingData = {
            "comList_val":str(comList_val.get()),
            "camList_val":str(camList_val.get()),
            "baud_val":str(baud_val.get()),
            "slider0Obj":str(objectX),
            "slider1Obj":str(objectW),
            "width":str(width),
            "height":str(height)
        }
        jsonPath = os.path.join(savePath, "save.json")
        with open(str(jsonPath), "w+") as f:
            json.dump(savingData, f)

    def goodbye():
        print('goodbye!')
        if thread1!= None and thread2!=None and thread3!= None != None and thread6 != None:
            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()
            thread6.join()
            
        killFlag.set()
        stateKill.set()
        threadKill.set()
        
        createJson()
        
        if cam != None:
            cam.release()
            
        exit()
            
    __initiate__()
    print('__LOG__ : exitted main function')
    goodbye()


class Hawk_Eye:
    preset_ready = False
    ALL_MODELS = {}
    model_display_name = ''
    model_handle = ''
    category_index = None

    def build_inputs_for_segmentation(image):
        """Builds segmentation model inputs for serving."""
        # Normalizes image with mean and std pixel values.
        image = normalize_image(image)
        return image


    def pathDef():
        global ALL_MODELS
        ALL_MODELS = {
        'material_model' : os.path.join(os.getcwd(),"sources","GoogleAPI","material_model", "saved_model","saved_model"),
        'material_form_model' : str(os.path.join(os.getcwd(), 'sources','GoogleAPI','material_form_model', 'saved_model', 'saved_model')),
        'plastic_model' : str(os.path.join(os.getcwd(),'sources','GoogleAPI','plastic_types_model', 'saved_model','saved_model'))
        }

        print('path creating process done')
        varDef()

    def varDef():
        global model_display_name, model_handle
        print('a) material model')
        print('b) material_form_model')
        print('c) plastic_model')
        print('')
        print('based on the input options above, please select the input')
        
        get_num = input('input > ')
        if get_num == 'a' or get_num == 'A':
            model_display_name = 'material_model'
            print(f'selected model is {model_display_name}')
            
        elif get_num == 'b' or get_num == 'B':
            model_display_name = 'material_form_model'
            print(f'selected model is {model_display_name}')
        
        elif get_num == 'c' or 'C':
            model_display_name = 'plastic_model'
            print(f'selected model is {model_display_name}')
        
        model_handle = ALL_MODELS[model_display_name]
        selection()


    def selection():
        
        
        global category_index, preset_ready
        
        
        print('Selected model:'+ model_display_name)
        print('Model Handle at TensorFlow Hub: {}'.format(model_handle))
        
        if model_display_name == 'material_model':
            PATH_TO_LABELS = os.path.join(os.getcwd(),"sources","labelmap", "material_labels.pbtxt")
        elif model_display_name == 'material_form_model':
            PATH_TO_LABELS = os.path.join(os.getcwd(),'hawk-eye-enging','googletf2', 'models','official','projects','waste_identification_ml','pre_processing','config','data','material_form_labels.pbtxt')
        elif model_display_name == 'plastic_model':
            PATH_TO_LABELS = os.path.join(os.getcwd(),'hawk-eye-enging','googletf2', 'models','official','projects','waste_identification_ml','pre_processing','config','data','plastic_model.pbtxt')

        print('Labels selected for',model_display_name)
        print('\n')
        category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
        print(category_index)
        
        print('values are preset are ready')
        preset_ready = True

    def load_model():
        global model
        # load model
        print('loading model...')
        model = tf.saved_model.load(model_handle)
        print('model loaded!')
        return model


    def run_inference_for_single_image(model, image):

        detection_fn = model.signatures['serving_default']
        height= detection_fn.structured_input_signature[1]['inputs'].shape[1]
        width = detection_fn.structured_input_signature[1]['inputs'].shape[2]
        
        input_size = (height, width)

        # image = np.asarray(image)

        image_np = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        # apply pre-processing functions which were applied during training the model
        image_np_cp = cv2.resize(image_np, input_size[::-1], interpolation = cv2.INTER_AREA)
        image_np = build_inputs_for_segmentation(image_np_cp)
        image_np = tf.expand_dims(image_np, axis=0)
        print('************************************************')
        print(type(image_np))

        image_np.get_shape()


        # Run inference
        output_dict = detection_fn(image_np)
        print(f'output dictionary : {output_dict}')

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop('num_detections'))
        print(f'number of detected obejct is {num_detections}')


        output_dict = {key: value.numpy() for key, value in output_dict.items()}
        
        label_id_offset = 0
        min_score_thresh =0.6
        use_normalized_coordinates=True
        
        output_dict['num_detections'] = num_detections

        if use_normalized_coordinates:
            # Normalizing detection boxes
            output_dict['detection_boxes'][0][:,[0,2]] /= height
            output_dict['detection_boxes'][0][:,[1,3]] /= width

        # detection_classes should be ints.
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
    
        # Handle models with masks:
        if 'detection_masks' in output_dict:
            # Reframe the the bbox mask to the image size.
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                                        output_dict['detection_masks'][0], output_dict['detection_boxes'][0], 1080,1920)      
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, np.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
        
        return output_dict
    def run_inference(model, category_index, cap):
        while True:
            ret, image_np = cap.read()
            # Actual detection.
            output_dict = run_inference_for_single_image(model, image_np)

            image_height, image_width, _ = image_np.shape

            print(f"{image_height} x {image_width}")

            # Visualization of the results of a detection.
            viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np,
                output_dict['detection_boxes'][0],
                (output_dict['detection_classes'][0] + 0).astype(int),
                output_dict['detection_scores'][0],
                category_index= category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=200,
                min_score_thresh=0.6,
                agnostic_mode= False,
                instance_masks=output_dict.get('detection_masks_reframed', None),
                line_thickness=4)

            cv2.imshow('object_detection', cv2.resize(image_np, (800, 600)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break


    def __init__():
        pathDef()
        if preset_ready == True:
            detection_model = load_model()
            print(f'category index is {category_index}')
        
        cap = cv2.VideoCapture(0)
        run_inference(detection_model, category_index, cap)


    __init__()
