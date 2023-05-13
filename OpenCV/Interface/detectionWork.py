# colour interface project

import tkinter as tk
import threading
import cv2
import numpy as np
from PIL import Image, ImageTk

threadKill = threading.Event()
camLock = threading.Lock()
detectionLock = threading.Lock()
std = None
selectedColour = None
img = None
imgtk = None
tkmg = None

# update video in priority

def vidUpdate():
    global vid,std
    vid = cv2.VideoCapture(0)
    while not threadKill.is_set():
        with camLock:
            global std
            ret, std = vid.read()


    

def _detection_():
    global red_lower_colour, red_upper_colour, blue_lower_colour, blue_upper_colour
    red_lower_colour = np.array([162,100,100])
    red_upper_colour = np.array([185,255,255])
    
    blue_lower_colour = np.array([104,50,100])
    blue_upper_colour = np.array([126,255,255])
    
    while not threadKill.is_set():
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
            if red[2]>90 and red[3]>90:          
                centerred = (2*red[0]+red[2])//2, (2*red[1]+red[3])//2
                for redVid in videos:
                    if selectedColour['red']:
                        print('red is true')
                        cv2.rectangle(redVid,(red[0],red[1]),(red[0]+red[2],red[1]+red[3]),(172,0,179),2)
                        cv2.circle(redVid, centerred, 1, (255,0,0) ,thickness=3)
                    else:
                        print('red is false')
        
        
        
        contourBlu, _2 = cv2.findContours(bottom_blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contourBlu:
            blu = cv2.boundingRect(contour)
            if blu[2]>90 and blu[3]>90:          
                centerBlu = (2*blu[0]+blu[2])//2, (2*blu[1]+blu[3])//2
                for bluVid in videos:
                    if selectedColour['blue'] == True:
                        print('blue is true')
                        cv2.rectangle(bluVid,(blu[0],blu[1]),(red[0]+blu[2],blu[1]+blu[3]),(172,0,179),2)
                        cv2.circle(bluVid, centerBlu, 1, (255,0,0) ,thickness=3)
                    else:
                        print('blue is false')
            
        for boxes in videos:
            cv2.rectangle(boxes, (590,410), (690,310), 2)
        cv2.circle(result, (360,640) , 5, (255,0,0), 3)
        frame = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        
        with detectionLock:
            global img
            img = Image.fromarray(frame)
            

def detectionInit():
    global thread6
    resolutionX = 1280
    resolutionY = 720
    displayWindow = tk.Toplevel()
    displayWindow.title("Detection Engine 1.0")
    displayWindow.geometry("1000x500")
    displayWindow.resizable(True,True)
    canvas = tk.Canvas(displayWindow, width= resolutionX, height=resolutionY)
    canvas.pack()
    canvas_image = canvas.create_image(0,50,anchor = tk.NW)
    
    print('detection initialized')
    
    if selectedColour == None:
        print('selectedColour is Nonetype')
        return
    else:
        thread6 = threading.Thread(target=_detection_)
        thread6.start()
    
    print('thread6 started ************** {}'.format(thread6.is_alive()))
    def updateCanvas():
        print('entered updatecanvas')
        if threadKill.is_set():
            displayWindow.destroy()
            return
        with detectionLock:
            global imgtk
            if img is not None:
                imgtk = ImageTk.PhotoImage(image=img)
                canvas.itemconfig(canvas_image, image = imgtk) 
                canvas.image = imgtk
        displayWindow.after(1000,updateCanvas)
    
    updateCanvas()
    print('end of detectioninit -- detection working // thread6 state is {}'.format(thread6.is_alive()))
    displayWindow.mainloop()
    
def colourInterface():
    global thread5
    
    thread5 = threading.Thread(target= vidUpdate)
    thread5.start()
    print(f'thread5 state is {thread5.is_alive()}')
    
    # create window for colourselection
    colourWindow = tk.Tk()
    colourWindow.title ('Colour Selection')
    colourWindow.geometry('300x300')
    colourWindow.resizable(True,True)
    
    colourSelectInfo = tk.Label(colourWindow, text=f'Please Select Colour')
    colourSelectInfo.place(x=30, y=15)
        
    global redOpt, BluOpt
    redOpt = tk.BooleanVar()
    BluOpt = tk.BooleanVar()
    
    
    def updateColour(redOpt, BluOpt):
        global selectedColour
        selectedColour= {'red': False, 'blue' : False}
        
        if redOpt:
            selectedColour['red'] = True
        else:
            selectedColour['red'] = False
            
        if BluOpt:
            selectedColour['blue'] = True
        else:
            selectedColour['blue'] = False
            
        print('updated selected colour\n')
        print(f'selected colour is {selectedColour}')
    
    redBtn = tk.Checkbutton(colourWindow,text='red',  variable=redOpt, onvalue= True, offvalue= False, command=lambda: updateColour(redOpt.get(),BluOpt.get()))
    BlueBtn = tk.Checkbutton(colourWindow, text='blue', variable= BluOpt, onvalue= True, offvalue= False, command=lambda: updateColour(redOpt.get(),BluOpt.get()))
    redBtn.place(x=30, y= 45)
    BlueBtn.place(x=130, y= 45)
    
    while type(std) == type(None):
        print('waiting for cam')
    
    nxtBtn = tk.Button(colourWindow, text='next', command=lambda: detectionInit())
    nxtBtn.place(x= 130, y=100)
    
    colourWindow.mainloop()




colourInterface()


print('exitting')
threadKill.set()
thread5.join()
thread6.join()

