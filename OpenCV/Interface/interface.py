import tkinter as tk
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk
import time


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
            arr.append(str(f'{index}'))
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

def saver(cam, com, len):
    serialCom = com
    
    i = 0
    if len > 1:
        while i < len:
            camera_Setting(camPort= cam[i])
            i+=1
    else:
        camera_Setting(camPort= cam)  
    
def __initiate__():
    delta = 0
    camPorts = searchPortCam()
    comPorts = searchSerialPort()
    ay =  100
    ayl = 80
    
    global window
    window = tk.Tk()
    window.title("Project Claw For Humanity Port Selector")
    window.geometry("600x240")
    window.resizable(True,True)
    
    comList_val = tk.StringVar(window, "Com Port")
    comList_val.set("Com Port")
    ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
    ComLable.place(x=30,y=20)
    ComOption = tk.OptionMenu(window, comList_val, *comPorts)
    ComOption.place(x= 30, y= 45)
        
    
    if len(camPorts) > 1:
        camList_val = {}
        variableText = {}
        variable = {}
        holder = {}
        print(f'cam port number greater than 0 // {len(camPorts)}')
        while len(camPorts) > delta:
            name = f"{delta}"
            camList_val[name] = tk.StringVar(window, "Cam Port")
            camList_val[name].set("Cam Port")
            variableText[name] = tk.Label(window,text=f'Select Camera {delta+1} Port', font=('Arial',15))
            variableText[name].place(x=30, y= ayl + (45*delta))
            variable[name] = tk.OptionMenu(window, camList_val[name], *camPorts)
            variable[name].place(x=30, y= ay + (45*delta))
            holder[delta] = camList_val[name].get()
            delta += 1

        btn = tk.Button(window, text='Next', command=lambda: saver(holder, comList_val.get(), len(camPorts)))
        btn.place(x= 40, y= (ay+ayl+45))
    else:
        CamPortLabel = tk.Label(window, text='Select Camera 1 Port', font=('Arial',15))
        CamPortLabel.place(x=30, y=ayl)
        camList_val = tk.StringVar(window, "Cam Port")
        camList_val.set("Cam Port")
        variable = tk.OptionMenu(window, camList_val, *camPorts)
        variable.place(x=30, y= ay)
        btn = tk.Button(window, text='Next', command=lambda: saver(camList_val.get(), comList_val.get(), len(camPorts)))
        btn.place(x= 40, y= 130)
    
    
    
    

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

def camVid(camWindow, standard, resolX, resolY):
    canvas = tk.Canvas(camWindow, width= resolX, height= resolY)
    canvas.place(x= 300, y= 300)
    while True:
        standard1 = cv2.cvtColor(standard, cv2.COLOR_BGR2RGB)
            # Convert the image to PIL format
        pil_img = Image.fromarray(standard1)

        # Convert the PIL image to a PIL.ImageTk.PhotoImage object
        photo_img = ImageTk.PhotoImage(pil_img)

        canvas.create_image(300,300, anchor ='nw', Image = photo_img)

        # return photo_img

passed = False
def __camInit__(selectedport, len, resolutionX, resolutionY):
    global passed, frontVid
    print(passed)
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
        print(f'entered elif statement passed state is {passed}\n')
   
        read, standard = frontVid.read()
        return standard
        

def update_video(ret, window, canvas, canvas_image,resX,resY):
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

inform = 0
def camDisplayer(selectedPort, len, resolutionX, resolutionY, windo):
    global inform
    ret = __camInit__(int(selectedPort), len, resolutionX, resolutionY)

    if inform == 0:
        ret = __camInit__(int(selectedPort), len, resolutionX, resolutionY)
        inform += 1

    else:
        pass

    canvas = tk.Canvas(windo, width=resolutionX, height=resolutionY)
    canvas.pack()
    canvas_image = canvas.create_image(0, 0, anchor=tk.NW)


    # update the video in a loop
    def update_loop():
        ret = __camInit__(int(selectedPort), len, resolutionX, resolutionY)
        update_video(ret, windo, canvas, canvas_image, resolutionX, resolutionY)
        # call this function again after 10ms
        windo.after(10, update_loop)
    update_loop()

                
        
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
    leftX.setvar('1000')
    leftX.place(x=30, y=30)
    rightX = tk.Entry(camWindow, width=4)
    rightX.setvar('1000')
    rightX.place(x=90,y=30)
    x = tk.Label(camWindow, text='X')
    x.place(x=79, y=33)
    
    
    
    btn = tk.Button(camWindow, text='search', command=lambda: camDisplayer(camPort, 1, leftX.get(), rightX.get(),windo= camWindow))
    btn.place(x= 30, y= 67)
    
    
    camWindow.mainloop()
    
    
    

__initiate__()

