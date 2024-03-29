import time
import tkinter as tk
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk
import threading
import numpy as np
import struct

thread1 = None
thread2 = None
thread3 = None
decodedData = None


def launcher():
    logo = tk.PhotoImage(file="/Users/changbeankang/Desktop/GitHub/Claw-For-Humanity/Com/logo/Picture2.png")
    global root
    root = tk.Tk()
    root.title("Project Claw For Humanity V1.0")

    logo = tk.PhotoImage(file="/Users/changbeankang/Desktop/GitHub/Claw-For-Humanity/Com/logo/Picture2.png")
    root.iconphoto(True, logo)
    logo = logo.subsample(2)
    logo_label = tk.Label(root, image=logo)
    logo_label.pack()
    root.geometry("300x300")  # Call __initiate__() through root.after()
    root.after(3000, __initiate__)
    root.mainloop()

def __initiate__(): # returns camport, comport and baudrate
    
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
    # window.iconphoto(True, logo)
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
    camWindow.resizable(True, True)
    
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
    comCall.place(x= 400, y= 150)

incomingState = False
stateKill = threading.Event()
checkStateLock = threading.Lock()
state = None

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

    def checkState(comWindow):
        while not stateKill.is_set():
            with checkStateLock:
                global state
                stateInfo = tk.Label(comWindow, text=f'current state is {state}')
                stateInfo.place(x=30, y=50)
                print(f'state is "{state}"')
                if state == 'serial is open':
                    Pass = tk.Button(comWindow, text='Next')
                    Pass.place(x=30, y=90)
                    break
            comWindow.update()  # update the GUI to show changes
            time.sleep(0.1)  # wait a short time before checking again
        


    thread3 = threading.Thread(target= checkState, args= (comWindow,))
    thread3.start()
    print(f'\n\nthread3 stat is {thread3.is_alive()}\n\n')
    
    cntBtn = tk.Button(comWindow, text= 'Connect', command=lambda: logOpen(communication))
    cntBtn.place(x= 30, y= 90)
    comWindow.mainloop()
    
    

def log(widget, message, level = 'INFO'):
    tag = level.upper()
    widget.insert(tk.END, message + "\n", tag)


def send(data):
    global serialInst, sent
    sent = data
    print(f'\n{data.encode()} is written\n')
    serialInst.write(f"{data}".encode())
    
    
receiveLock = threading.Lock()

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
            if sent == decodedData:
                print('matching data')
                with checkStateLock:
                    global state
                    state = 'connected'
            else:
                print('line 321 // something is weird')
                print(f'[trace] sent is {sent}')
                print(f'[trace] decoded data is {decodedData}')
                print(f'state is {state}')
            
        elif incomingState == False: 
            log(text_widget, f'waiting for incoming bytes from arduino')

        loggingbox.after(1000, update_gui) 

logOpeni = 0

def logOpen(communication):
    global serialInst, text_widget,loggingbox,thread2, logOpeni
    serialInst = serial.Serial(port=str(communication[0]),baudrate= int(communication[1]))
    
    if serialInst.is_open:
        with checkStateLock:
            global state
            state = 'serial is open'
    
    else:
        with checkStateLock:
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
    nxt_btn = tk.Button(loggingbox, text='send', command=lambda: send(str(enter_widget.get())), width= 2)
    nxt_btn.place(x=20, y= 90)
    enter_widget.pack()
    
    log(text_widget, "communication established and waiting for response")

    thread2 = threading.Thread(target=receive, args=(serialInst,))
    thread2.start()
    log(text_widget, f"thread called and thread state is {thread2.is_alive}")
        
    loggingbox.after(10, update_gui)
 

        
def colourSelect():
    print('colourselect')
        
__initiate__()

killFlag.set()
stateKill.set()
if thread1!= None and thread2!=None and thread3!= None:
    thread1.join()
    thread2.join()
    thread3.join()
exit()