import tkinter as tk
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk

debugVar = 0

def searchPortCam():
    index = 0
    global arr
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def searchSerialPort():
    #variable
    HWID = []
    i=0
    ports = list(serial.tools.list_ports.comports())
    
    if len(ports) == 0:
        HWID.append("No Ports Available")
    else:
        while i<len(ports):
            port = ports[i]
            HWID.append(f"Name: {port.device} || Description: {port.description}")
            i+=1
    
    print(HWID[0])
    return HWID

camport = None
comport = None

def saver(var, var1):
    global camport, comport
    comport = var
    camport = var1
    print(f'selected camport is {camport}')
    camera_Setting(camPort= camport)
    
  

def initSave(camPort, comPort):
    camera = int(camPort)
    comunication = comPort
    

def __initiate__():
    camPorts = searchPortCam()
    comPorts = searchSerialPort()
    ay =  100
    ayl = 80
    
    global window
    window = tk.Tk()
    window.title("Project Claw For Humanity Port Selector")
    window.geometry("600x240")
    window.resizable(True,True)
    
    
    
    camList_val = tk.StringVar(window, "Cam Port")
    camList_val.set("Cam Port")
    comList_val = tk.StringVar(window, "Com Port")
    comList_val.set("Com Port")
    
    if len(camPorts)>1:
        delta = 0
        variable = {}
        variableText = {}
        print(f'cam port number greater than 0 // {len(camPorts)}')
        while len(camPorts)>= delta:
            name = f"camLable{delta}"
            variableText[name] = tk.Label(window,text=f'Select Camera {delta} Port', font=('Arial',15))
            variableText[name].place(x=30, y = ayl +(45*delta))
            variable[name] = tk.OptionMenu(window, camList_val, *camPorts)
            variable[name].place(x=30, y= ay+(45*delta))
            delta+=1
        btn = tk.Button(window, text='Next', command=lambda: saver(comList_val, camList_val))
        btn.place( x= 40, y= (ay+ayl+45) )
    else:
        CamPortLabel = tk.Label(window, text='Select Camera 1 Port', font=('Arial',15))
        CamPortLabel.place(x=30, y=ayl)
        btn = tk.Button(window, text='Next', command=lambda: saver(comList_val.get(), camList_val.get()))
        btn.place(x= 40, y= 130)
    
    
    camOption = tk.OptionMenu(window, camList_val, *camPorts)
    camOption.place(x=30, y=ay)
    
    ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
    ComLable.place(x=30,y=20)
    ComOption = tk.OptionMenu(window, comList_val, *comPorts)
    ComOption.place(x= 30, y= 45)
    
    

    window.mainloop()
        
def colourInterface():
    ColourWindow = tk.Tk()
    ColourWindow.title("Project Claw For Humanity Main")
    ColourWindow.geometry("1000x800")
    ColourWindow.resizable(True,True)
    # colours and buttons
    redBtn = tk.Button(ColourWindow, text='red')
    redBtn.place(x= 100, y= 100)
    bluBtn = tk.Button(ColourWindow, text='blue')
    bluBtn.place(x= 200, y= 100)
    yelBtn = tk.Button(ColourWindow, text = 'green')
    yelBtn.place()

def camVid(frontVid):
    read, standard = frontVid.read()
    standard1 = cv2.cvtColor(standard, cv2.COLOR_BGR2RGB)
        # Convert the image to PIL format
    pil_img = Image.fromarray(standard1)

    # Convert the PIL image to a PIL.ImageTk.PhotoImage object
    photo_img = ImageTk.PhotoImage(pil_img)

    return photo_img
    

def __camInit__(selectedport, len, resolutionX, resolutionY):
    if len == 1:
        frontVid = cv2.VideoCapture(selectedport)
        
        if frontVid.isOpened():
            print('[LOG]: frontvid is open')
            frontVid.set(cv2.CAP_PROP_FRAME_WIDTH, resolutionX)
            frontVid.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutionY)
        else:
            tk.messagebox.showinfo(title='Error', message='Front Camera encountered problem')
            exit()
            
            
        while True:
            camVid(frontVid)
        


    else:
        i=0
        svr = {}
        while i<=len:
            name = f'video{i}'
            svr[name] = cv2.VideoCapture(i)
            if not svr[name].isOpened():
                tk.messagebox.showinfo(title='Error', message=f'Camera {name} encountered problem')
            else:
                svr[name].set(cv2.CAP_PROP_FRAME_WIDTH, resolutionX)
                svr[name].set(cv2.CAP_PROP_FRAME_HEIGHT, resolutionY)
                i+=1
    
def camDisplayer (selectedPort, len, resolutionX, resolutionY):
    selectedPort = int(selectedPort)
    while True:
        cv2.imshow('display',__camInit__(selectedPort, len, resolutionX, resolutionY))
    
        
def camera_Setting(camPort):
    global window
    window.destroy()
    
    # create window
    camWindow = tk.Tk()
    camWindow.title("Camera Setting")
    camWindow.option_add("*Font","Ariel 15")
    camWindow.geometry("1000x500")
    camWindow.resizable(True, True)
    
    # entry
    infoRes = tk.Label(camWindow, text='Width x Height for camera')
    infoRes.place(x=30, y=5)
    leftX = tk.Entry(camWindow, width=4)
    leftX.place(x=30, y=30)
    rightX = tk.Entry(camWindow, width=4)
    rightX.place(x=90,y=30)
    x = tk.Label(camWindow, text='X')
    x.place(x=79, y=33)
    
    
    
    btn = tk.Button(camWindow, text='search')
    btn.place(x= 30, y= 67)
    btn.config(command=camDisplayer(camPort, len(arr), leftX, rightX))
    
    
    camWindow.mainloop()
    
    
    

__initiate__()

