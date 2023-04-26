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
        global g,comPorts,camPorts, ComOption, baudOption, HWID, HWID_DEVICE
        g +=1
        HWID, HWID_DEVICE = searchSerialPort()
        camPorts = searchPortCam() # search comports
        comPorts = HWID
        
        ComOption = tk.OptionMenu(window, comList_val, *comPorts)
        baudOption = tk.OptionMenu(window, baud_val, *baudRates)
        ComOption.place(x= ax, y= 45)
        baudOption.place(x= ax, y= 100)
        
        print(f'receiveVal happened {g} times')
        window.after(3000, receiveVal)
        
        
    receiveVal()
    
    
    # happens only if there are more than 1 camera 
    # multiple cameras on hold for now
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
    # create variable
    errorReTry = 0
    
    # kill window
    global window
    window.destroy()
    
    # save 3 variables
    camPort = camPort
    comPort = comPort
    bdrate = bdrate
    
    # tempo work
    cam = cv2.VideoCapture(int(camPort))

    if not cam.isOpened():
        print(f'camera encountered problem // line 165 // unknown issue // tried {errorReTry}')
        cam = cv2.VideoCapture(int(camPort))
        errorReTry += 1
        
        if errorReTry == 3:
            tk.messagebox.showinfo(title= 'warninig', message = 'camera encountered problem // line 165 // unknown issue // exitting')
            exit()
        camera_Setting(int(camPort), comPort, bdrate)
        
    else:
        print('camera captured successfully \n')
        frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    
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
    
    btn = tk.Button(camWindow, text='search', command=lambda: camDisplayer(camPort, 1, int(leftX.get()), int(rightX.get()),camWindow, comPort, bdrate))
    btn.place(x= 30, y= 67)
    
    
    camWindow.mainloop()

def camDisplayer(camPort, len, resolutionX, resolutionY, windo, comport, bdrate):
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
    
    # if state == 'connected':
    #     print('connected')
    #     nxtBtn = tk.Button(comWindow, text='next', command=lambda: detection(__camInit__(int(camPort), len, resolutionXT, resolutionYT)))
    #     nxtBtn.place(x=30, y =200)
    # else:
    #     comWindow.update()
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
    log(text_widget,message=f'threadstate is {thread1.is_alive}')
    log(text_widget, message=f'serial state is {serialInst.in_waiting}')
    receive.after(10000, connect(portName, bdrate))

def receiver(portName, bdrate):
    
    global receive,ri,thread1,text_widget,serialInst
    ri+=1
    
    print(f'openwindow is {openwindow}')
        
    if openwindow == True:
        receive = tk.Tk()
        receive.title('incoming data logger')
        receive.resizable(False, False)
        text_widget = tk.Text(receive, height=20, width=80)
        text_widget.pack()
        serialInst = serial.Serial(str(portName), int(bdrate))
        if serialInst.is_open:
            print('successfully connected')
        else:
            print('failed to connect')
        
    elif openwindow == False:
        print('openWindow is False')
        print(f'the state of serial is {serialInst.is_open}')
    else:
        print('this is not possible')
    
    receiveBool = False
        
    log(text_widget, 'looking for incoming bytes')
    receiveBoolLock = threading.Lock()
    
    def checker(serialInst):
        print('thread started -- checker() \n \n')
        error = 0
        nonlocal receiveBool
        with receiveBoolLock:
            receiveBool = True    
            print(f'checker initiated + receiveBool Status is {receiveBool}')
        
        while not stopflag.is_set():
            # print('checker in progress')
            print(f'{serialInst.in_waiting}')
            if type(serialInst) != type(None):
                if serialInst.in_waiting > 0:
                    print('feed from arduino detected \n')
                    incoming = serialInst.read(serialInst.in_waiting)
                    decoded = incoming.decode('utf-8')
                    print(f'incoming bytes from Arduino: {decoded} \n')
                    log(text_widget, message=f'incoming bytes from Arduino: {decoded}')
                    
                elif serialInst.in_waiting ==0:
                    print('waiting for feed')
                else:
                    print('this is impossible')
            else:
                
                print(f'serialInst type is None! encountered problem {serialInst}')
                error+=1
                if error == 50:
                    print('error happened 50 times')
                    thread1.join()
                    
                    
                

    thread1 = threading.Thread(target= checker, args=(serialInst))
    thread1.start()
    
    
    print(f'thread state is {thread1.is_alive}')
    
    # Call after() on the text widget to schedule mid_organizer after the mainloop
    text_widget.after(500, mid_organizer, portName, bdrate)
    
    receive.mainloop()


def connect(portName, bdrate):
    print('connect function initiated')
    global serialInst, j, receive, text_widget
    
    # state = 'not connected'
    serialInst = serial.Serial(str(portName), int(bdrate))
    
    
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

colors = {}
colorReturn = {}
selectedColours = {}
def detection(camera, selectedcolour):
    read, standard = camera.read()
    
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
    


# receiver()
__initiate__()