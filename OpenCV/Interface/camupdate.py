import time
import tkinter as tk
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk
import subprocess
import threading
import numpy as np


decodedData = None

def launcher():
    global root
    
    root = tk.Tk()
    root.title("Project Claw For Humanity V1.0")

    logo = tk.PhotoImage(file="/Users/changbeankang/Desktop/GitHub/Claw-For-Humanity/Com/logo/Picture2.png")
    root.iconphoto(True, logo)
    logo = logo.subsample(2)
    logo_label = tk.Label(root, image=logo)
    logo_label.pack()
    root.geometry("300x300")
    
    root.after(1000, __initiate__)  # Call __initiate__() through root.after()
    root.mainloop()


def __initiate__(): # returns camport, comport and baudrate
    # global root
    # root.destroy()
    print('entered initiate')
    
    # create variables
    global window
    baudRates = [300,1200,2400,9600,10417,19200,57600,115200]
    defaultLocX = 30 # default x location 
    defaultLocY = 150
    defaultLocExpl = 130
    
    # create window using tkinter
    window = tk.Tk()
    window.title("Project Claw For Humanity Port Selector")
    window.geometry("600x240")
    window.resizable(True,True)
    
    comList_val = tk.StringVar(window, "Com Port")
    ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
    ComLable.place(x=defaultLocX,y=20)
    
    baud_val = tk.StringVar(window,"Baud Rate")
    baudLable = tk.Label(window, text="Select Baud Rate", font=('Arial', 15))  
    baudLable.place(x= defaultLocX, y= 80)    
    
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
    
    global window
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
    global camWindow
    camWindow = tk.Tk()
    camWindow.title("Camera Setting")
    camWindow.option_add("*Font","Ariel 15")
    camWindow.geometry("1000x500")
    camWindow.resizable(False, False)
    
    # entry
    subTitle = tk.Label(camWindow, text='Width x Height for camera')
    subTitle.place(x=30, y=5)
    
    width = tk.Entry(camWindow, width=4)
    width.place(x=30, y=30)
    height = tk.Entry(camWindow, width=4)
    height.place(x=90,y=30)
    x = tk.Label(camWindow, text='X')
    x.place(x=79, y=33)
    
    recommend = tk.Label(camWindow, text=f'recommended camera resolution is {int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))}')
    recommend.place(x= 113, y= 69)
    
    btn = tk.Button(camWindow, text='search', command=lambda: camDisplayer(int(width.get()), int(height.get()), communication))
    btn.place(x= 30, y= 67)
    
    camWindow.mainloop()

cam_lock = threading.Lock()

std = None
killFlag = threading.Event()

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
        displayResX = int(resolutionX) / 2
        displayResY = int(resolutionY) / 2
    else:
        displayResX = resolutionX
        displayResY = resolutionY
        
    print('about to start thread')
    threadVid()
    print('successfully initiated thread')
    canvas = tk.Canvas(camWindow, width=displayResX, height=displayResY)
    canvas.pack()
    canvas_image = canvas.create_image(0, 50, anchor=tk.NW)
    print('canvas created')
    # comCall = tk.Button(camWindow, text='next', command=lambda: __initCom__(comport, bdrate))
    # comCall.place(x= 400, y= 300)

    # update the video in a loop
    def update_canvas():
        with cam_lock:
            if not type(std) == None:
                pic = std.copy()
            else:
                pass
    

        frame = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (int(displayResX),int(displayResY)))
            
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        canvas.itemconfig(canvas_image, image = imgtk)
        canvas.image = imgtk
        camWindow.after(1000,update_canvas)
            
    
    print('updateing canvas..')
    update_canvas()
    
    comCall = tk.Button(camWindow, text='next', command=lambda: __initCom__(communication))
    comCall.place(x= 400, y= 300)

incomingState = False
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

    stateInfo = tk.Label(comWindow, text=f'current state is {state}')
    stateInfo.place(x=30, y=50)

    if state == "connected":
        print('current state is "connected"')
        nxtBtn = tk.Button(comWindow, text= "next", command=lambda: detect())
        nxtBtn.place(x=30, y= 170)
    
    cntBtn = tk.Button(comWindow, text= 'Connect', command=lambda: logOpen(communication))
    sendBtn = tk.Button(comWindow, text='Send', command=lambda: send("1"))
    nxtBtn = tk.Button(comWindow, text="next", command= lambda: colourChoice())
    nxtBtn.place(x=20, y= 120)
    
    
    sendBtn.place(x=30, y= 130)
    cntBtn.place(x= 30, y= 90)
    camWindow.mainloop()

def detect():
    print('state connected')

def log(widget, message, level = 'INFO'):
    tag = level.upper()
    widget.insert(tk.END, message + "\n", tag)


def send(str):
    global serialInst
    serialInst.write(f"{str}".encode())
    print(f'\ncurrent state of thread1 is {thread1.is_alive}\n')
    print(f'\ncurrent state of thread2 is {thread2.is_alive}\n')
    log(text_widget, f"serialInst inwaiting is {serialInst.in_waiting}")
    
receiveLock = threading.Lock()
incomeSave = ()
decoded = {}
incoming = {}
def receive(serialInst):
    n = 0
    while not killFlag.is_set():
        if type(serialInst) != type(None):
            if serialInst.in_waiting > 0:
                print('feed from arduino detected \n')
                incoming = serialInst.read(serialInst.in_waiting)
                decoded = incoming.decode('utf-8')
                with receiveLock:
                    global decodedData, incomingState, incomeSave
                    incomeSave = incoming
                    if not decoded == None:
                        n+=1
                        incomingState = True
                        decodedData = decoded
                    else:
                        incomingState = False
                        decodedData = None
                n+=1
                        
        
def update_gui():
    with receiveLock:
        global decodedData, incomingState
        if incomingState == True:
            log(text_widget, f'incoming bytes from arduino {decodedData}')
        elif incomingState == False: 
            log(text_widget, f'waiting for incoming bytes from arduino')
        checkComponent = decodedData
    
        
    print(f'decoded data is {incomeSave}')
    
    
    global loggingbox
    loggingbox.after(1000,update_gui)

    
def logOpen(communication):
    print('entered logOpen')
    global state, serialInst, text_widget,loggingbox,thread2
    serialInst = serial.Serial(port=str(communication[0]),baudrate= int(communication[1]))
    
    if serialInst.is_open:
        state = 'serial is open'
    else:
        state = 'serial is not open'
        tk.messagebox.showinfo(title = 'warning', message = 'serial cannot be opened. Please check the port')
        return
    
    loggingbox = tk.Tk()
    loggingbox.title('logger')

    loggingbox.geometry("1000x1000")
    loggingbox.resizable(True,True)
    text_widget = tk.Text(loggingbox, height=20, width=80)
    text_widget.pack()
    enter_widget = tk.Entry(loggingbox, width= 18)
    nxt_btn = tk.Button(loggingbox, text='send', command=lambda: send(enter_widget.get()), width= 2)
    nxt_btn.place(x=20, y= 90)
    enter_widget.pack()
    
    
    
    log(text_widget, "waiting for incoming bytes...")

    print('thread about to start')
    thread2 = threading.Thread(target=receive, args=(serialInst,))
    thread2.start()
    print(f'thread started and thread state is {thread2.is_alive}')
    
    
    loggingbox.after(10, update_gui)

def coulourReturn(colour):
    global selectedColours
    selectedColours = []
    selectedColours.append(str(colour))

def colourChoice():
    global comWindow, colourSelect
    comWindow.destroy()
    colourSelect = tk.Tk()
    colourSelect.title('ColourSelect - project CFH')
    colourSelect.geometry("1000x700")
    colourSelect.resizable(True, True)
    
    selectedColour = tuple("red")
    
    red = tk.Button(colourSelect, text='red', command= lambda: detection(selectedColour)) # set command
    red.place(x=30, y= 100)
    blue = tk.Button(colourSelect, text= 'blue', command= lambda:detection(tuple("blue"))) # set command
    blue.place(x=90, y=100)
    colourSelect.mainloop()



def colourRange (color):
    if color == 'red':
        red_lower_colour = np.array([162,100,100])
        red_upper_colour = np.array([185,255,255])
        return red_lower_colour, red_upper_colour
    elif color == 'blue':
        blue_lower_colour = np.array([104,50,100])
        blue_upper_colour = np.array([126,255,255])
        return blue_lower_colour, blue_upper_colour
    elif color == 'green':
        green_lower_colour = np.array([33,50,50])
        green_upper_colour = np.array([40,255,255])
        return green_lower_colour, green_upper_colour

def mskCombine(downTotal):
    setmskComb = len(downTotal) - 1
    counter = 0
    savor = {}
    
    while setmskComb > 0:
        if counter != len(downTotal):
            if counter == 0:
                savor[counter] = cv2.bitwise_or(downTotal[setmskComb], downTotal[setmskComb-1])
                
            else:
                savor[counter] = cv2.bitwise_or(savor[counter-1],downTotal[setmskComb-1])
                
        counter += 1
        setmskComb -= 1

    finalCombined = savor[counter-1]
    return finalCombined

def detection(selectedcolour):
    with cam_lock:
        global std
        standard = std
        icol = 0
        icol2 = 0
        icol3 = 0
        tankDown ={}
        tankUp = {}
        
        maskTotal =()
        maskSave = {}
        
        tankDownTotal = ()
        tankUpTotal = ()
        
        
        while icol <= len(selectedcolour):
            
            tankDown[icol] = colourRange(selectedcolour(icol))(0)
            tankUp[icol] = colourRange(selectedcolour(icol))(1)
            
            tankDownTotal = tankDownTotal + (tankDown[icol],)
            tankUpTotal = tankUpTotal + (tankUp[icol],)
            
            icol += 1
        
        bottomHsv = cv2.cvtColor(standard, cv2.COLOR_BGR2HSV)
        
        
        while icol2 <= len(tankDownTotal):
            maskSave[icol2] = cv2.inRange(bottomHsv, tankDownTotal[icol2], tankUpTotal[icol2])
            maskTotal = maskTotal + (maskSave[icol2],)
            icol2 += 1 
        
        combined_mask = mskCombine(maskTotal)
        
        result = cv2.bitwise_and(standard, mask= combined_mask)
        
        videos = [result, combined_mask]
        
        if len(selectedcolour) > 1:
            contours = {}
            
            while len(selectedcolour) >= icol3:
                # draw boxes
                contours[icol3], _1 = cv2.findContours(tankDown[icol3], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours[icol3]:
                    global colors, colorReturn, selectedColours
                    selectedColours[icol3] = cv2.boundingRect(contour)
                    # sender('red', red1)
                    if selectedColours[icol3][2]>90 and selectedColours[icol3][3]>90:          
                        centerred = (2*selectedColours[icol3][0]+selectedColours[icol3][2])//2, (2*selectedColours[icol3][1]+selectedColours[icol3][3])//2
                        print('')
                        for redVid in videos:
                            cv2.rectangle(redVid,(selectedColours[icol3][0],selectedColours[icol3][1]),(selectedColours[icol3][0]+selectedColours[icol3][2],selectedColours[icol3][1]+selectedColours[icol3][3]),(172,0,179),2)
                            cv2.circle(redVid, centerred, 1, (255,0,0) ,thickness=3)
                icol3 += 1
                
        elif len(selectedcolour) == 1:      
            contours2, _2 = cv2.findContours(tankDown[0], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours2:
                global colors, colorReturn
                colour1 = cv2.boundingRect(contour)
                if colour1[2]>90 and colour1[3]>90:
                    centerblue = (2*colour1[0]+colour1[2])//2, (2*colour1[1]+colour1[3])//2
                    # sender('blue', blue1)
                    for blueVid in videos:
                        cv2.rectangle(blueVid,(colour1[0],colour1[1]),(colour1[0]+colour1[2],colour1[1] + colour1[3]),(0,255,255),2)
                        cv2.circle(blueVid, centerblue, 1, (255,0,0) ,thickness=3)
                        # sender('blue')
        else:
            print("this ain't possible")
            exit()

        # make a box at wanted region
        for boxes in videos:
            cv2.rectangle(boxes,(590,410), (690,310), (0,0,255), 2) # change box location depending on target area
        
        # center pixel hsv value
        centerBottomHsv = bottomHsv[360,640]
        
        #print(centerBottomHsv)
        # make a circle
        cv2.circle(result, (360,640) , 5, (255,0,0), 3)
        #print(colour)
        
        
    
    print('entered detection.')    

        
        
        
__initiate__()

killFlag.set()
thread1.join()
thread2.join()
