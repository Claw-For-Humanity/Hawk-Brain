
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import tkinter as tk
import argparse
import imutils
import threading
from PIL import Image, ImageTk
import time
from tkinter import messagebox

class Hawk_brain_plugin_v4:
    cam = cv2.VideoCapture(0)
    threadKill = threading.Event()
    camLock = threading.Lock()
    def ___init__():
        thread1 = threading.Thread(target= Hawk_brain_plugin_v4.Camwork)
        print('[thread1] camwork initiated')

    def camWork():
        while not Hawk_brain_plugin_v4.threadKill.is_set():
            ret, frame = Hawk_brain_plugin_v4.cam.read()
            if ret:
                with Hawk_brain_plugin_v4.camLock:
                    global pic,stat
                    pic = frame.copy()
                    stat = ret
            else:
                print('cam not ready!')
                pass
    
    def interface():
        global camInterface 
        camInterface = tk.Tk()
        camInterface.title('Detection Interface')
        camInterface.geometry('400x530')
        camInterface.resizable(True, True)            
        
        button_initiate = tk.Button(camInterface, text= 'start', command=Hawk_brain_plugin_v4.CaptureInterface)
        button_initiate.place(x= 30, y= 100)
        
        camInterface.mainloop()

    def captureInterface():
        global defCaptureStat,captureWindow,initWindowKilled
        print('entered capture default frame')
        
        # create window
        captureWindow = tk.Tk()
        captureWindow.title('capture window')
        captureWindow.geometry("2000x1300")
        
        # create canvas
        canvas = tk.Canvas(captureWindow, width=1920, height=1080)
        canvas.place(x=30,y=60)
        canvas_image = canvas.create_image(0, 50, anchor=tk.NW)
        print('canvas created') 

        # update the video in a loop
        def update_canvas():
            print('updating canvas on new window')
            print(f'\ngoodbye window state is {goodbyeWindow}\n')
            if not defCaptureStat:
                with Hawk_brain_plugin_v4.camLock:
                    if stat:
                        frame = pic.copy()
                    
                    else:
                        print('error / cam stat is none') 
                        pass
        
                frame = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (int(1920),int(1080)))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                canvas.itemconfig(canvas_image, image = imgtk)
                canvas.image = imgtk
            print('done')
            captureWindow.after(10,update_canvas)

        def checkKill():
            global captureWindow, compare_ready
            print('entered checkKill')
            print(f'goodbyewindow state is {goodbyeWindow}')
            
            if goodbyeWindow: 
                print('attempting windowkill')
                captureWindow.destroy()
                print(f'capture window state is {captureWindow}')
                captureWindow = None
                if captureWindow == None:
                    print('window is completely destroyed')
                    Hawk_brain_plugin_v4.init_compare()
                else:
                    captureWindow.after(10, checkKill)
            else:
                print('line 125 -- standby for goodbye window')
                captureWindow.after(100, checkKill)
        
        def captureDef():
            global defImage, defCaptureStat
            print('capturing default frame')
            
            defCaptureStat = True
            def set_windowKill():
                global goodbyeWindow
                goodbyeWindow = True
                checkKill()
            nextBtn = tk.Button(captureWindow, text="next", command=set_windowKill)
            nextBtn.place(x=80, y=30)
            resetBtn = tk.Button(captureWindow, text="reset", command=Hawk_brain_plugin_v4.reset)
            resetBtn.place(x = 150, y= 30)

            with Hawk_brain_plugin_v4.camLock:
                if stat:
                    defImage = pic.copy()
                else:
                    print('check cam status')
                    pass
            
            captureWindow.after(10, checkKill)
            
        # capture button
        captureBtn = tk.Button(captureWindow,text="capture", command= captureDef)
        captureBtn.place(x=30, y=30)  
        
        update_canvas()