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
    
    time.sleep(1)
    # initiate camera interface
    if cam_thread.is_alive():
        main_interface()

def camWork():
    global pic, stat
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
        pic = pic
        stat = stat
      
def main_interface():
    print('\nentered main interface\n')
    # define internal thread variables
    main_internal_threadKill = threading.Event()
    main_internal_threadPause = threading.Event()
    
    global main_tk_detection
    
    # create interface
    main_tk_detection = tk.Tk()
    main_tk_detection.title('Detection Interface')
    main_tk_detection.geometry('2000x1300')
    
    # create canvas
    main_canvas = tk.Canvas(main_tk_detection, width=1920, height=1080)
    main_canvas.place(x=30,y=60)
    main_canvas_image = main_canvas.create_image(0, 50, anchor=tk.NW)
    

    def internal_thread_manager():
        # internal_thread1 = threading.Thread(target= main_update_canvas)
        internal_thread2 = threading.Thread(target= main_check_kill)
        # internal_thread1.start()
        internal_thread2.start()

        main_update_canvas()

        print('both thread started')
        time.sleep(0.5)

    def main_update_canvas():
        global default_image
        if not main_internal_threadKill.is_set():
            if not main_internal_threadPause.is_set():
                print('entered main_update_canvas')
                with camLock:
                    if stat:
                        default_image = pic.copy()
                    else:
                        tk.messagebox.showinfo(titie = 'warning', message = 'not possible @ line 95')            
                default_image = default_image
            main_tk_detection.after(10,main_update_canvas)
    
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
        
        with camLock:
            if stat:
                default_image = pic.copy()
            else:
                tk.messagebox.showinfo(title = 'warning', message = 'something is wrong - line 123')          
        
        default_image = default_image
        default_image_state = True
        
        main_nextBtn = tk.Button(main_tk_detection, text="next", command=main_check_kill)
        main_nextBtn.place(x=80, y=30)
        
        main_resetBtn = tk.Button(main_tk_detection, text="reset", command=main_reset)
        main_resetBtn.place(x = 150, y= 30)
    
    main_captureBtn = tk.Button(main_tk_detection,text="capture", command= capture)
    main_captureBtn.place(x=30, y=30)  


    internal_thread_manager()



def exitter():
    threadKill.set()
    print('threadkill set')
    exit()

__init__()

exitter()
