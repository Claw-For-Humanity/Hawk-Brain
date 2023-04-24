import tkinter as tk
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk
import subprocess
import threading
import time
import numpy as np



# Create global variables
debugVar = 0
passed = False
inform = 0
HWID_DEVICE = []
HWID = []

def dicCheck(dictionary, chkVal):
    current = 0
    while current < len(dictionary):
        if not chkVal == dictionary[current]:
            current += 1
        else:
            print(current)
            break
    return current 

g = 0
# Step 1: 1st screen, select camport and comport
def __initiate__():
    # create variables
    global window
    delta = 0 # count how many cameras there are
    
    # create window using tkinter
    window = tk.Tk()
    window.title("Project Claw For Humanity Port Selector")
    window.geometry("600x240")
    window.resizable(True,True)
    
    
    baudRates = [300,1200,2400,9600,10417,19200,57600,115200]
    ax = 30 # default x location for camera entry
    ay =  150 # default location for camera entry
    ayl = 130 # default location for camera entry explanation
    
    # Select comport and camport
    comList_val = tk.StringVar(window, "Com Port")
    comList_val.set("Com Port")
    ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
    ComLable.place(x=ax,y=20)
    
    
    
    baud_val = tk.StringVar(window,"Baud Rate")
    baud_val.set("Baud Rate")
    baudLable = tk.Label(window, text="Select Baud Rate", font=('Arial', 15))  
    baudLable.place(x= ax, y= 80)    
    
    
    
    def receiveVal():
        global g,comPorts,camPorts, ComOption, baudOption
        g +=1
        HWID, HWID_DEVICE = searchSerialPort()
        camPorts = searchPortCam() # search comports
        comPorts = HWID
        
        
        ComOption = tk.OptionMenu(window, comList_val, *comPorts)
        baudOption = tk.OptionMenu(window, baud_val, *baudRates)
        ComOption.place(x= ax, y= 45)
        baudOption.place(x= ax, y= 100)
        
        print(f'receiveVal happened {g} times')
        window.after(1000, receiveVal)
        
    
    

    receiveVal()
    

    
    # happens only if there are more than 1 camera 
    if len(camPorts) > 1:
        # create local variables
        camList_val = {}
        variableText = {}
        variable = {}
        holder = {}
        
        # happens only if there are more than 1 camera
        while len(camPorts) > delta:
            name = f"{delta}"
            camList_val[name] = tk.StringVar(window, "Cam Port")
            camList_val[name].set("Cam Port")
            variableText[name] = tk.Label(window,text=f'Select Camera {delta+1} Port', font=('Arial',15))
            variableText[name].place(x=ax, y= ayl + (45*delta))
            variable[name] = tk.OptionMenu(window, camList_val[name], *camPorts)
            variable[name].place(x=ax, y= ay + (45*delta))
            holder[delta] = camList_val[name].get()
            delta += 1
        # button calls saver
        btn = tk.Button(window, text='Next', command=lambda: camera_Setting(holder, comList_val.get(), baud_val.get()))
        btn.place(x= ax+10, y= (ay+ayl+45))
    else:
        CamPortLabel = tk.Label(window, text='Select Camera 1 Port', font=('Arial',15))
        CamPortLabel.place(x=ax, y=ayl)
        camList_val = tk.StringVar(window, "Cam Port")
        camList_val.set("Cam Port")
        variable = tk.OptionMenu(window, camList_val, *camPorts)
        variable.place(x=ax, y= ay)
        btn = tk.Button(window, text='Next', command=lambda: camera_Setting(camList_val.get(), comList_val.get(),baud_val.get()))
        btn.place(x= ax+10, y= 200)
    
    window.mainloop()

# for __initiate__() // search comport and camport
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
    #variable
    global HWID_DEVICE, HWID
    HWID_DEVICE = []
    HWID = []
    i=0
    ports = list(serial.tools.list_ports.comports())

    if len(ports) == 0:
        HWID.append("No Ports Available")
    else:
        while i<len(ports):
            port = ports[i]
            HWID_DEVICE.append(port.device)
            HWID.append(f"Name: {port.device} || Description: {port.description}")
            i+=1
    return HWID, HWID_DEVICE

# setting for camera -> set resolution, camera preview
def camera_Setting(camPort, comPort, bdrate):
    # tempo work
    tempo = cv2.VideoCapture(int(camPort))

    if not tempo.isOpened():
        tempo = cv2.VideoCapture(int(camPort))
        camera_Setting(int(camPort), comPort, bdrate)
    else:
        frame_width = int(tempo.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(tempo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # kill window
    global window
    window.destroy()
    
    # create window
    global camWindow
    camWindow = tk.Tk()
    camWindow.title("Camera Setting")
    camWindow.option_add("*Font","Ariel 15")
    camWindow.geometry("1000x500")
    camWindow.resizable(False, False)
    
    
    # entry
    infoRes = tk.Label(camWindow, text='Width x Height for camera')
    infoRes.place(x=30, y=5)
    
    leftX = tk.Entry(camWindow, width=4)
    leftX.place(x=30, y=30)
    
    rightX = tk.Entry(camWindow, width=4)
    rightX.place(x=90,y=30)
    
    x = tk.Label(camWindow, text='X')
    x.place(x=79, y=33)
    
    recRes = tk.Label(camWindow, text=f'recommended camera resolution is {frame_width}x{frame_height}')
    recRes.place(x= 113, y= 69)
    
    btn = tk.Button(camWindow, text='search', command=lambda: camDisplayer(camPort, 1, leftX.get(), rightX.get(),camWindow, comPort, bdrate))
    btn.place(x= 30, y= 67)
    
    
    camWindow.mainloop()

def camDisplayer(camPort, len, resolutionX, resolutionY, windo, comport, bdrate):

    resolutionX = int(resolutionX)
    resolutionY = int(resolutionY)
    global inform
    ret = __camInit__(int(camPort), len, resolutionX, resolutionY)
    if inform == 0:
        ret = __camInit__(int(camPort), len, resolutionX, resolutionY)
        inform += 1
    else:
        pass
    
    if resolutionX or resolutionY > 1000:
        resolutionXT = int(resolutionX) / 2
        resolutionYT = int(resolutionY) / 2
    else: 
        resolutionXT = resolutionX
        resolutionYT = resolutionY
    
    canvas = tk.Canvas(windo, width=resolutionXT, height=resolutionYT)
    canvas.pack()
    canvas_image = canvas.create_image(0, 50, anchor=tk.NW)

    print(f'comport is {comport}')
    print(f'bdrate is {bdrate}')
    
    comCall = tk.Button(windo, text='next', command=lambda: __initCom__(comport, bdrate))
    comCall.place(x= 400, y= 300)

    # update the video in a loop
    def update_loop():
        ret = __camInit__(int(camPort), len, resolutionXT, resolutionYT)
        update_video(ret, canvas, canvas_image, resolutionXT, resolutionYT)
        # call this function again after 10ms
        windo.after(10, update_loop)
    update_loop()
    
def __camInit__(selectedport, len, resolutionX, resolutionY):
    global passed, frontVid
    
    if passed == False:
        if len == 1:
            frontVid = cv2.VideoCapture(selectedport)
            print(f'x = {resolutionX} // y = {resolutionY}')
            if resolutionX and resolutionY:
                resolutionX = float(resolutionX)
                resolutionY = float(resolutionY)
            else:
                print(f'resolution not set {resolutionX} and {resolutionY}')
                tk.messagebox.showinfo(title='Error', message = 'Resolution box empty')
            
            if frontVid.isOpened():
                print('[LOG]: frontvid is open')
                frontVid.set(cv2.CAP_PROP_FRAME_WIDTH, resolutionX)
                frontVid.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutionY)
                passed = True
                __camInit__(selectedport, len, resolutionX, resolutionY)
            else:
                tk.messagebox.showinfo(title='Error', message='Front Camera encountered problem')
                return 'error'
                    
    elif passed == True:
        read, standard = frontVid.read()
        return standard

def update_video(ret, canvas, canvas_image,resX,resY):
    # Convert the frame from BGR to RGB
    frame = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)

    # Resize the frame to fit the size of the canvas
    frame = cv2.resize(frame, (int(resX), int(resY)))

    # Convert the frame to a PIL image
    img = Image.fromarray(frame)

    # Convert the PIL image to a Tkinter image
    imgtk = ImageTk.PhotoImage(image=img)
  
    # Update the canvas with the new image
    canvas.itemconfig(canvas_image, image=imgtk)
    canvas.image = imgtk

state = None

serialInst = None

def __initCom__(comPort, baudrate):
    global camWindow,state
    state = 'checking connection'
    camWindow.destroy()
    
    global comWindow
    comWindow = tk.Tk()
    comWindow.title("ComPort checker")
    comWindow.option_add("*Font","Ariel 15")
    comWindow.geometry("1000x500")
    comWindow.resizable(False, False)
    
    where = dicCheck(HWID, comPort)
    portInfo = tk.Label(comWindow, text=f'comport connection check // selected comport is {HWID_DEVICE[where]} // selected baud rate is {baudrate}')
    portInfo.place(x=30, y=15)
    
    stateInfo = tk.Label(comWindow, text=f'current state is {state}')
    stateInfo.place(x=30, y=50)
    
    cntBtn = tk.Button(comWindow, text= 'Connect', command=lambda: threadStart(HWID_DEVICE[where], baudrate))
    
    cntBtn.place(x= 30, y= 90)
    
    if state == 'connected':
        print('connected')
        nxtBtn = tk.Button(comWindow, text='next', command=lambda: openConsole(HWID_DEVICE[where]))
        nxtBtn.place(x=30, y =200)
    else:
        comWindow.update()
j=0

openwindow = False
ri = 0


def threadStart(portName, bdrate):

    global receive,openwindow,stopflag
    stopflag = threading.Event()
    
    if ri > 0:
        if receive.state() == 'normal':
            openwindow = False    
            receiver(portName, bdrate)
    else:
        print('line 329 // entered else statement')
        openwindow = True
        receiver(portName, bdrate)
        
    print("receiver funtions exited")
    stopflag.set()
    thread1.join()
    print(f'trying to kill thread \n thread state is {thread1.is_alive}')

    
def log(widget, message, level='INFO'):
    tag = level.upper()
    widget.insert(tk.END, message + "\n", tag)

def mid_organizer(portName, bdrate):
    global receive
    log(text_widget, 'aftter mainloop 500 millisec')
    log(text_widget, 'after mainloop 10000 millisec, run connect')
    receive.after(10000, connect(portName, bdrate))

def receiver(portName, bdrate):
    
    global receive,ri,thread1,text_widget
    ri+=1
    
    
    
    
    print(f'openwindow is {openwindow}')
        
    if openwindow == True:
        receive = tk.Tk()
        receive.title('incoming data logger')
        receive.resizable(False, False)
        text_widget = tk.Text(receive, height=20, width=80)
        text_widget.pack()

        
    elif openwindow == False:
        print('openWindow is False')
    else:
        print('this is not possible')
    
    receiveBool = False
        
    log(text_widget, 'looking for incoming bytes')
    receiveBoolLock = threading.Lock()
    
    def checker():
        print('thread started -- checker() \n \n')
            
        nonlocal receiveBool
        with receiveBoolLock:
            receiveBool = True    
            print(f'checker initiated + receiveBool Status is {receiveBool}')
                    
        print('line 388 // thread check')
        
        while not stopflag.is_set():
            # print('checker in progress')
            if type(serialInst) != type(None):
                if serialInst.in_waiting > 0:
                    print('feed from arduino detected \n')
                    incoming = serialInst.read(serialInst.in_waiting)
                    decoded = incoming.decode('utf-8')
                    print(f'incoming bytes from Arduino: {decoded} \n')
                    
                    log(text_widget, message=f'incoming bytes from Arduino: {serialInst.read(serialInst.in_waiting).decode()}')
            else:
                print('waiting for feed')
                time.sleep(3)

    print('line 396 // thread initialized')
    thread1 = threading.Thread(target= checker)
    thread1.start()
    
    print('line 389 // thread1 initiated')
    
    print(f'thread state is {thread1.is_alive}')
    
    time.sleep(8)
    
    print('mainloop enter \n')
    
    # Call after() on the text widget to schedule mid_organizer after the mainloop
    text_widget.after(500, mid_organizer, portName, bdrate)
    
    receive.mainloop()
    
    
    
    
    

   

    


def connect(portName, bdrate):
    print('connect function initiated')
    global serialInst, j, receive, text_widget
    
    # state = 'not connected'
    serialInst = serial.Serial(str(portName), int(bdrate))
    
    serialInst.port = str(portName)
    serialInst.baudrate = int(bdrate)
    
    if serialInst.is_open:
        print(f"{serialInst} is open")
        state = 'serialInst is open'   
    
    # elif not serialInst.is_open:
    #     print('serial opening failed')
    #     tk.messagebox.showinfo(title= 'error', message= 'opening port failed!')
    #     comWindow.update()
    #     state = 'cannot be opened'
    #     return state
    # else:
    #     state = 'successfully opened'
    #     pass
    
    
    send = 3
    serialInst.write(bytes(f'{send}'.encode()))
    print(f"{send} is successfully sent to \n {serialInst}")
    
    
    text_widget.after(5000, mid_organizer, portName, bdrate)
    # comWindow.update()
    # return state

def openConsole(port):
    global comWindow
    comWindow.destroy()
    
    global consl, main
    consl = tk.Tk()
    consl.title("Console for Arduino")
    consl.option_add("*Font","Ariel 15")
    consl.geometry("1000x500")
    consl.resizable(False, False)
    
    main = tk.Tk()
    main.title("main program for eagle")
    main.option_add("*Font","Ariel 15")
    main.geometry("500x500")
    main.resizable(True, True)
    
    text_widget = tk.Text(consl)
    text_widget.pack(fill='both', expand= True)
    
    # Create the subprocess to run the Arduino CLI and get the serial port name
    process = subprocess.Popen(['arduino', '--monitor', '--getpref', 'serial.port'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Get the serial port name from the output of the subprocess
    serial_port = process.stdout.readline().strip()

    # Create the subprocess to open the Arduino console
    console = subprocess.Popen(['arduino', '--monitor', f'--port={str(port)}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    def read_from_console():
        # Read a line of output from the console subprocess
        line = console.stdout.readline()

        # If the subprocess has terminated, stop reading output
        if console.poll() is not None:
            return

        # Append the output to the Tkinter Text widget
        text_widget.insert('end', line)

        # Schedule the next read in 10 milliseconds
        consl.after(10, read_from_console)

    # Schedule the first read in 10 milliseconds
    consl.after(10, read_from_console)
    comWindow = tk.Text()        
    
    
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

def detection(camera, selectedcolour):
    read, standard = camera.read()
    icol = 0
    tank ={}
    while icol <= len(selectedcolour):
        tank[icol] = 
    
    if selectedcolour == 'Red':
        colourRange
    
    
    print('entered detection.')    
    


# receiver()
__initiate__()