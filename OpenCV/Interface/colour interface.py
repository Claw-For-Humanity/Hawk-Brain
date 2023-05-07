# colour interface project

import tkinter as tk
import threading

def colourInterface():
    colourWindow = tk.Tk()
    colourWindow.title ('Colour Selection')
    colourWindow.geometry('1000x800')
    colourWindow.resizable(True,True)
    
    colourSelectInfo = tk.Label(colourWindow, text=f'Please Select Colour')
    colourSelectInfo.place(x=30, y=0)
    
    updateLock = threading.Lock()
        
    global redOpt, BluOpt
    redOpt = tk.BooleanVar()
    BluOpt = tk.BooleanVar()
    
    def updateColour():
        global redOpt, BluOpt, selectedColour
        
        selectedColour=()
        
        if redOpt:
            selectedColour.__add__('red')
        elif not redOpt:
            selectedColour.__reduce__('red')
        
        if BluOpt:
            selectedColour.__add__('blue')
        elif not BluOpt:
            selectedColour.__reduce__('blue')
        
        
    
    redBtn = tk.Checkbutton(colourWindow,text='red',  variable=redOpt, onvalue= True, offvalue= False, command= lambda: updateColour())
    BlueBtn = tk.Checkbutton(colourWindow, text='blue', variable= BluOpt, onvalue= True, offvalue= False, command= lambda: updateColour())
    redBtn.place(x=30, y= 30)
    BlueBtn.place(x=60, y= 30)
    
    colourWindow.mainloop()

colourInterface()