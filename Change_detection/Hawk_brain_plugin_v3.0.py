# requires to install
# pip install --upgrade scikit-image
# pip install --upgrade imutils


# working on threads


import cv2
from skimage.metrics import structural_similarity as compare_ssim
import tkinter as tk
import argparse
import imutils
import threading
from PIL import Image, ImageTk
import time
from tkinter import messagebox


# image values
default_image = None

# tkinter variables
main_tk_detection = None

# state variables
main_killWindow = False
default_image_state = False

# thread variables
threadKill = threading.Event()
threadPause = threading.Event()
camLock = threading.Lock()

# camera vars
cam = cv2.VideoCapture(0)
stat = None
pic = None

# thread 1 = camWork

def __init__():
    # initiate camera work
    cam_thread = threading.Thread(target= camWork)
    cam_thread.start()
    print ('\ncamwork thread initiated\n')
    
    # initiate camera interface
    main_interface()
    

def camWork():
    while not threadKill.is_set():
        print('camwork thread working')
        ret, frame = cam.read()
        if ret:
            with camLock:
                global pic,stat
                pic = frame.copy()
                stat = ret
                print('camwork thread working, stat is {}'.format(stat))
        else:
            tk.messagebox.showinfo(title = 'Warning', message = 'No Camera Avail.')
            pass

def main_interface():
    print('\nentered main interface\n')
    # define internal thread variables
    main_internal_threadKill = threading.Event()
    main_internal_threadPause = threading.Event()
    
    global main_tk_detection
    
    main_tk_detection = tk.Tk()
    main_tk_detection.title('Detection Interface')
    main_tk_detection.geometry('2000x1300')
    
    main_canvas = tk.Canvas(main_tk_detection, width=1920, height=1080)
    main_canvas.place(x=30,y=60)
    main_canvas_image = main_canvas.create_image(0, 50, anchor=tk.NW)
    
    def internal_thread_manager():
        internal_thread1 = threading.Thread(target= main_update_canvas)
        internal_thread2 = threading.Thread(target= main_check_kill)
        internal_thread1.start()
        internal_thread2.start()
        print(f'internal thread 1 state is {internal_thread1.is_alive()}')
        
        print('both thread started')
    
    def main_update_canvas():
        while not main_internal_threadKill.is_set():
            print('entered main_update_canvas')
            with camLock:
                if stat:
                    default_image = pic.copy()
                else:
                    tk.messagebox.showinfo(titie = 'warning', message = 'not possible @ line 95')            
    
    def main_check_kill():
        global main_tk_detection
        while not main_internal_threadKill.is_set():
            # print('main check kill')
            if main_internal_threadPause.is_set():
                time.sleep(0.5)
                return
            if main_killWindow:
                print('attempting windowkill')
                main_tk_detection.destroy()
                print(f'capture window state is {main_tk_detection}')
            else:
                pass
        
    def main_reset():
        print('entered reset')
        
    def capture():
        global default_image, default_image_state
        default_image_state = True
        with camLock:
            if stat:
                default_image = pic.copy()
            else:
                tk.messagebox.showinfo(title = 'warning', message = 'something is wrong - line 123')            
        main_nextBtn = tk.Button(main_tk_detection, text="next", command=main_check_kill)
        main_nextBtn.place(x=80, y=30)
        main_resetBtn = tk.Button(main_tk_detection, text="reset", command=main_reset)
        main_resetBtn.place(x = 150, y= 30)
    
    main_captureBtn = tk.Button(main_tk_detection,text="capture", command= capture)
    main_captureBtn.place(x=30, y=30)  

    # using main thread to update canvas
    while not threadKill.is_set():
        if threadPause.is_set():
            time.sleep(0.5)
            return
        with camLock:
            print('stat and pic is ')
            print('pic = {}'.format(pic))
            print('stat = {}'.format(stat))
            while pic == None or stat == None:
                print('waiting for pic and stat to update')
                print(f'pic is {pic}')
                print(f'stat is {stat}')
            if stat:
                frame = pic.copy()
            else:
                tk.messagebox.showinfo(title= 'warning', message= 'something is wrong')
        frame = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (int(1920),int(1080)))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        main_canvas.itemconfig(main_canvas_image, image = imgtk)
        main_canvas.image = imgtk

    internal_thread_manager()
    main_tk_detection.after(10,)



def exitter():
    threadKill.set()
    print('threadkill set')
    exit()

__init__()

exitter()
