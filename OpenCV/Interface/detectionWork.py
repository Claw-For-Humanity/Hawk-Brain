# colour interface project

import tkinter as tk
import threading
import cv2
import numpy as np

threadKill = threading.Event()
camLock = threading.Lock()
colourUpdateLock = threading.Lock()
std = None
redKillThread = threading.Event()
blueKillThread = threading.Event()

def vidUpdate():
    vid = cv2.VideoCapture(0)
    while not threadKill:
        with camLock:
            global std
            ret, std = vid.read()

def colourInterface():
    # start thread
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
        while not threadKill.is_set():
            
            selectedColour= {'red': False, 'blue' : False}
            
            if redOpt.get():
                selectedColour['red'] = True
                if redKillThread.is_set():
                    redKillThread.clear()
            else:
                selectedColour['red'] = False
                if not redKillThread.is_set():
                    redKillThread.set()
                
            if BluOpt.get():
                selectedColour['blue'] = True
                if blueKillThread.is_set():
                   blueKillThread.clear() 
            else:
                selectedColour['blue'] = False
                if not blueKillThread.is_set():
                    blueKillThread.set()
        
            with colourUpdateLock:
                global detectionColour
                detectionColour = selectedColour
    
    thread4 = threading.Thread(target=updateColour, args=(redOpt, BluOpt))
    thread4.start()
    _detection_()
    
    
    redBtn = tk.Checkbutton(colourWindow,text='red',  variable=redOpt, onvalue= True, offvalue= False, command= lambda: updateColour())
    BlueBtn = tk.Checkbutton(colourWindow, text='blue', variable= BluOpt, onvalue= True, offvalue= False, command= lambda: updateColour())
    redBtn.place(x=30, y= 45)
    BlueBtn.place(x=130, y= 45)
    
    
    colourWindow.mainloop()

def variableContainer():
    
    global red_lower_colour, red_upper_colour, blue_lower_colour, blue_upper_colour
    red_lower_colour = np.array([162,100,100])
    red_upper_colour = np.array([185,255,255])
    
    blue_lower_colour = np.array([104,50,100])
    blue_upper_colour = np.array([126,255,255])


def _detection_():
    variableContainer()
    if std != None:
        pass
    else:
        _detection_()
    with camLock:
        bottomHsv = cv2.cvtColor(std, cv2.COLOR_BGR2HSV)
        
        bottom_red_mask = cv2.inRange(bottomHsv, red_lower_colour, red_upper_colour)
        bottom_blue_mask = cv2.inRange(bottomHsv, blue_lower_colour, blue_upper_colour)
        
        combinedMask = cv2.bitwise_or(bottom_red_mask, bottom_blue_mask)
        
        result = cv2.bitwise_and(std, std, mask= combinedMask)
        videos = [result, combinedMask]
        
        cv2.imshow('test', videos)
        

colourInterface()





