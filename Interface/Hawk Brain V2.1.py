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
savePath = os.getcwd() + "/json"

# json data
comList_val = None 
camList_val = None
baud_val = None
slider0Obj = None
slider1Obj = None
width = None
height = None

if not os.path.exists(os.getcwd() + "/json"):
    print('no previous directory')
    os.makedirs(os.getcwd() + "/json")
    saver = {}

else:
    print('else entered')
    if os.path.exists(os.getcwd()+ "/json/save.json"):
        f = open(os.getcwd()+ "/json/save.json")
        prevData = json.load(f)
        print('prev Data detected')
        print(f'prev = {prevData}')
        print('data are set')
        comList_val = prevData['comList_val']
        camList_val = prevData['camList_val']
        baud_val = prevData['baud_val']
        objectX = prevData['slider0Obj']
        objectW = prevData['slider1Obj']
        width = prevData['width']
        height = prevData['height']
        
    print('save path is {}'.format(savePath))
    

jsons = os.listdir(str(os.getcwd() + "/json"))
print(f"json file list : {jsons}")


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
    if comList_val is not None:
        comList_val = tk.StringVar(window, str(comList_val))
    
    else:
        print('comlist val is none')
        comList_val = tk.StringVar(window, "Com Port")
    ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
    ComLable.place(x=defaultLocX,y=20)
    
    if baud_val is not None:
        baud_val = tk.StringVar(window, str(baud_val))
    else:
        baud_val = tk.StringVar(window, "Baud Rate")
    baudLable = tk.Label(window, text="Select Baud Rate", font=('Arial', 15))  
    baudLable.place(x= defaultLocX, y= 80)
    if camList_val is not None:
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
    btn = tk.Button(window, text='Next', command=lambda: camera_Setting(camList_val.get(), comList_val.get(),baud_val.get()))
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
        camera_Setting(int(camPort), comPort, bdrate)
    
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
    
    if width is not None:
        width.insert(0,prevData["width"])
    else:
        pass
        
    if height is not None:
        height.insert(0,prevData["height"])
    else:
        pass
    
    x = tk.Label(camWindow, text='X')
    x.place(x=79, y=33)
    
    alta = 0
    def adjust_resolution(width, height, communication, window): 
        global alta
        if alta == 0:
            alta += 1
            return
        else:
            pass
        print('entered adjust resolution')
        
        camDisplayer(width, height, communication)
        
    
    recommend = tk.Label(camWindow, text=f'recommended camera resolution is {int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))}')
    recommend.place(x= 113, y= 79)
    
    btn = tk.Button(camWindow, text='search', command=lambda: adjust_resolution(int(width.get()), int(height.get()), communication, camWindow))
    btn.place(x= 30, y= 77)
    
    camWindow.mainloop()

def threadVid():
    global thread1
    print('thread entered')
    def update():
        global std 
        while not killFlag.is_set():
            ret, frame = cam.read()
            with cam_lock:
                if ret:
                    std = frame.copy()
    thread1 = threading.Thread(target=update)
    print('thread defined')
    thread1.start()
    print('thread started')
    print(f'thread state is {thread1.is_alive}')

def camDisplayer(resolutionX, resolutionY, communication):
    global width, height
    width = resolutionX
    height = resolutionY
    print('entered camdisplayer')
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
    print('resolution is set')        
    if resolutionX or resolutionY > 1000:
        displayResX = int(resolutionX) - 300
        displayResY = int(resolutionY) - 300
    else:
        displayResX = resolutionX
        displayResY = resolutionY
    
    camWindow.geometry(f"{resolutionX + 400 }x{resolutionY + 400}")
    print('about to start thread')
    threadVid()
    print('successfully initiated thread')
    canvas = tk.Canvas(camWindow, width=displayResX, height=displayResY)
    canvas.pack()
    
    canvas_image = canvas.create_image(0, 50, anchor=tk.NW)
    print('canvas created')

    # update the video in a loop
    def update_canvas():
        with cam_lock:
            if not type(std) == type(None):
                pic = std.copy()
            else:
                pass
    
        frame = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (int(displayResX),int(displayResY)))
            
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        canvas.itemconfig(canvas_image, image = imgtk)
        canvas.image = imgtk
        camWindow.after(10,update_canvas)
            
    
    print('updateing canvas..')
    update_canvas()
    
    comCall = tk.Button(camWindow, text='next', command=lambda: __initCom__(communication))
    comCall.place(x= 400, y= 150)

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
    
    cntBtn = tk.Button(comWindow, text= 'Connect', command=lambda: logOpen(communication))
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
    while not killFlag.is_set():
        if type(serialInst) != type(None):
            if serialInst.in_waiting > 0:
                decoded = serialInst.readline().decode().strip() # Read data from the serial port
                with receiveLock:
                    global decodedData, incomingState
                    if decoded != None:
                        incomingState = True
                        decodedData = decoded
                    else:
                        incomingState = False
                        decodedData = None
                        
def update_gui():
    with receiveLock:
        global decodedData, incomingState, loggingbox
        if incomingState == True:
            log(text_widget, f'incoming bytes from arduino {decodedData}')
            
        elif incomingState == False: 
            log(text_widget, f'waiting for incoming bytes from arduino')

        # check incoming data every second
        loggingbox.after(1000, update_gui) 

def logOpen(communication):
    
    comWindow.destroy()
    global serialInst, text_widget,loggingbox,thread2
    print('about to start thread 2')
    serialInst = serial.Serial(port=str(communication[0]),baudrate= int(communication[1]))
    thread2 = threading.Thread(target=receive, args=(serialInst,))
    thread2.start()
    
    print(f'thread 2 is started state is : {thread2.is_alive()}')
    
    
    loggingbox = tk.Tk()
    loggingbox.title('logging box')   
    
    with receiveLock:
        if decodedData == None:
            print('check arduino')
            nxt_btn = tk.Button(loggingbox, text="next", command=lambda: colourInterface())
            nxt_btn.place(x=40, y=90)
        else:
            pass
            
    

    loggingbox.geometry("1000x1000")
    loggingbox.resizable(True,True)
    text_widget = tk.Text(loggingbox, height=20, width=80)
    text_widget.pack()
    enter_widget = tk.Entry(loggingbox, width= 18)
    snd_btn = tk.Button(loggingbox, text='send', command=lambda: send(str(enter_widget.get())), width= 2)
    snd_btn.place(x=20, y= 90)
    enter_widget.pack()
    
    log(text_widget, "communication established and waiting for response")

    
    log(text_widget, f"thread called and thread state is {thread2.is_alive}")
        
    loggingbox.after(10, update_gui)
  
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
        with detectionLock:
            global ptBlue
            ptBlue = None
    
    def resetRed():
        with detectionLock:
            global ptRed
            ptRed = None
    
    # start thread for boxcheck
    thread4 = threading.Thread(target= boxCheck)
    thread4.start()
    
    while not threadKill.is_set():
        def lineColour(distance):
            if distance is not None:
                if distance >= 0: # blue
                    return (0,0,255)
                elif distance < 0:
                    return(0,255,0) # red
            else:
                pass
            
        def calcLineCenter(point1, point2):
            center = (int((point1[0] + point2[0])/2),int((point2[1] + point2[1])/2 + 10))
            return center
            
        with camLock:
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
                        with detectionLock:
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
                        with detectionLock:
                            global ptBlue
                            ptBlue = centerBlu
                            # ptBlue = (int((bx+bw)/2), int((by+bh)/2))
                    else:
                        resetblu()
            
        readyDetection = True
        
        centerObj = int(objectX+ (0.5 * objectW)),int(objectY + (0.5 * objectH))
        
        with distanceLock:
            if boxCheckStat == True:
                dR = distanceCalc("red", ptRed)
                dB = distanceCalc("blue",ptBlue)
                
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
        with detectionLock:
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
    push_object = 1
    pull_object = 2
    while readyDetection == False:
        print('boxCheck waiting for __detection__')
    
    while not threadKill.is_set():
        with detectionLock:
            global ptBlue
            objectBlue = ptBlue
            objectRed = ptRed

        with distanceLock:
            global boxCheckStat, distanceBlu, distanceRed
            boxCheckStat = True
            distanceBlu = distanceCalc("blue",ptBlue)
            distanceRed = distanceCalc("red",ptRed)
        
        print(f'objectblue is {ptBlue}')
        
        if type(objectBlue) != type(None):
            if distanceBlu <= 0:
                print('\n\n blue point polygon test less than 0: = ')
                print(f'distance between blue and object is{distanceBlu}')
                
                send_safety(push_object)    
            
            else:
                send(pull_object)
        
        else:
            send(pull_object)
        
        if type(objectRed) != type(None):
            if distanceRed <= 0:
                print('\n\n red point polygon test less than 0: = ')
                print(f'distance between red and object is{distanceRed}')
                send(push_object)
            
            else:
                send(pull_object)
        else:
            send(pull_object)

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
    
    thread6 = threading.Thread(target=_detection_)
    thread6.start()
    
    def updateCanvas():
        print('entered updatecanvas')
        if threadKill.is_set():
            displayWindow.destroy()
            return
        with detectionLock:
            global imgtk
            if img is not None:
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
        objectX = int(slider1.get())
        print(f'ObjectX is {objectX}\n')
        objectW = int(slider0.get())
        print(f'ObjectW is {objectW}\n')
        objectCS = int(slider2.get())
        print(f'objectCS is {objectCS}')
    
    
    slider0Info = tk.Label(colourWindow, text=f'width')
    slider0Info.place(x=30, y=200)
    
    slider1Info = tk.Label(colourWindow, text=f'X value')
    slider1Info.place(x=30, y=150)
    
    slider2Info = tk.Label(colourWindow, text=f'command sending distance')
    slider2Info.place(x=30, y=250)
    
    # slider 0 - x value
    slider0 = tk.Scale(colourWindow,variable=slider0Obj, orient= HORIZONTAL, from_=0, to=1280, command= updateScale)
    if objectX is not None:
        slider0.set(int(objectX))
    else:
        slider0.set(200)
    slider0.place(x = 30, y= 230)
    
    # slider 1 - width
    slider1 = tk.Scale(colourWindow,variable=slider1Obj, orient= HORIZONTAL, from_=0, to=1270, command= updateScale)
    if objectW is not None:
        slider1.set(int(objectW))
    else:
        slider1.set(900)
    slider1.place(x = 30, y= 175)
    
    # slider 2 - command sending distance
    slider2 = tk.Scale(colourWindow, variable=slider2Obj, orient= HORIZONTAL, from_= 0, to= 700, command= updateScale)
    slider2.place(x= 30, y= 285)
    
    
    updateBtn = tk.Button(colourWindow, text='update', command=lambda: updateScale())
    updateBtn.place(x= 30, y= 300)
    redBtn = tk.Checkbutton(colourWindow, text='red', variable=(redOpt), command= lambda: updateRedColour())
    BlueBtn = tk.Checkbutton(colourWindow, text='blue',variable=(BluOpt), command= lambda: updateBlueColour())

    
    redBtn.place(x=30, y= 45)
    BlueBtn.place(x=130, y= 45)
    
    while type(std) == type(None):
        print('waiting for cam')
    
    nxtBtn = tk.Button(colourWindow, text='next', command=lambda: detectionInit())
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
    
    if cam is not None:
        cam.release()
        
    exit()
        

__initiate__()
print('__LOG__ : exitted main function')
goodbye()