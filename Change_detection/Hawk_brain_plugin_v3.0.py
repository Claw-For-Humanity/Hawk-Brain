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
returnFrame_current = None
returnFrame_default = None

# tkinter variables
main_tk_detection = None
compare_interface = None

# state variables
main_killWindow = False
default_image_state = False
compare_ready = False

# thread variables
threadKill = threading.Event()
threadPause = threading.Event()
camLock = threading.Lock()
compareLock = threading.Lock()

# camera vars
cam = cv2.VideoCapture(0)
stat = None
pic = None

# canvas vars
main_canvas = None
main_canvas_image = None

compare_canvas = None
compare_canvas_image = None

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
        # print('camwork thread working')
        ret, frame = cam.read()
        if ret:
            with camLock:
                global pic,stat
                pic = frame.copy()
                stat = ret
                # print('camwork thread working, stat is {}'.format(stat))
        else:
            tk.messagebox.showinfo(title = 'Warning', message = 'No Camera Avail.')
            pass
        pic = pic
        stat = stat

internal_thread1 = None
internal_thread2 = None
main_internal_threadKill = None
main_internal_threadPause = None

def main_interface():
    global internal_thread1, internal_thread2, main_internal_threadKill, main_internal_threadPause
    
    print('\nentered main interface\n')
    # define internal thread variables
    main_internal_threadKill = threading.Event()
    main_internal_threadPause = threading.Event()
    
    global main_tk_detection, main_canvas, main_canvas_image
    
    # create interface
    main_tk_detection = tk.Tk()
    main_tk_detection.title('Detection Interface')
    main_tk_detection.geometry('2000x1300')
    
    # create canvas
    main_canvas = tk.Canvas(main_tk_detection, width=1920, height=1080)
    main_canvas.place(x=30,y=60)
    main_canvas_image = main_canvas.create_image(0, 50, anchor=tk.NW)

    def internal_thread_manager():
        global internal_thread1, internal_thread2
        internal_thread1 = threading.Thread(target= main_update_canvas)
        internal_thread2 = threading.Thread(target= main_check_kill)
        internal_thread1.start()
        internal_thread2.start()

        # main_update_canvas()

        print('both thread started')
        time.sleep(0.5)

    def main_update_canvas():
        print('\n\nmain update canvas entered\n\n')

        global default_image, main_canvas, main_canvas_image, main_tk_detection
        
        while not main_internal_threadKill.is_set():
            if not main_internal_threadPause.is_set() and not default_image_state:
                print('passed thread checks')
                
                # receive frames
                with camLock:
                    if stat:
                        main_frame = pic.copy()
                    else:
                        tk.messagebox.showinfo(titie = 'warning', message = 'not possible @ line 95')            
                
                main_frame = main_frame               
                main_frame = cv2.cvtColor(main_frame, cv2.COLOR_BGR2RGB)
                main_frame = cv2.resize(main_frame, (int(1920),int(1080)))
                main_image = Image.fromarray(main_frame)
                main_image_tk = ImageTk.PhotoImage(image= main_image)
                main_canvas.itemconfig(main_canvas_image, image= main_image_tk)
                main_canvas.image= main_image_tk
            
            print(f'operation complete, another main tk detection || threadkill state is {main_internal_threadKill.is_set()}')
    
    def main_check_kill():
        print('entered main check kill')
        global main_tk_detection
        while not main_internal_threadKill.is_set():
            # print('main check kill')
            if main_internal_threadPause.is_set():
                time.sleep(0.5)
                return
            if main_killWindow:
                # main_internal_threadKill.set()
                
                print('attempting windowkill')
                
                main_tk_detection.destroy()
            else:
                pass
        
    def main_reset():
        print('entered reset')
        
    def capture():
        
        global default_image, default_image_state, main_killWindow
        
        with camLock:
            if stat:
                default_image = pic.copy()
            else:
                tk.messagebox.showinfo(title = 'warning', message = 'something is wrong - line 123')          
        
        default_image = default_image
        default_image_state = True
        
        main_nextBtn = tk.Button(main_tk_detection, text="next", command=init_compare)
        main_nextBtn.place(x=80, y=30)
        
        main_resetBtn = tk.Button(main_tk_detection, text="reset", command=main_reset)
        main_resetBtn.place(x = 150, y= 30)
    
    main_captureBtn = tk.Button(main_tk_detection,text="capture", command= capture)
    main_captureBtn.place(x=30, y=30)  


    internal_thread_manager()
    print('\n\ndone!\n\n')
    main_tk_detection.mainloop()

def init_compare():
    global main_killWindow, compare_interface, compare_canvas, compare_canvas_image, compare_threadKill, compare_threadPause, main_internal_threadPause, main_internal_threadKill
    
    # kill window var
    # main_killWindow = True
    main_internal_threadPause.set()
    
    main_internal_threadKill.set()
    
    print(f'main kill window is set to {main_killWindow}')
    print('\ninitiating comparison process\n')
    
    # create thread vars
    compare_threadKill = threading.Event()
    compare_threadPause = threading.Event()

    # comparison interface creation
    compare_interface = tk.Tk()
    compare_interface.title('Compare Plugin v3.0')
    compare_interface.geometry("1200x1000")
    compare_interface.resizable(True,True)
    
    # create canvas
    compare_canvas = tk.Canvas(compare_interface)
    compare_canvas.place(x=30, y=30)
    compare_canvas_image = compare_canvas.create_image(0,50,anchor=tk.NW)
    
    # define update canvas
    def compare_update_canvas():
        global compare_ready
        print('entered compare update canvas @ line 216')
        while compare_ready != True:
            print('wait! - line 219')
<<<<<<< Updated upstream
            time.sleep(1)
        while not compare_threadKill :
            if not compare_threadPause:
=======
            time.sleep(10)
        while not compare_threadKill.is_set():
            if compare_threadPause.is_set():
>>>>>>> Stashed changes
                print('passed thread check -- line 218')
                with compareLock:
                    currentFrame = returnFrame_current
                    defaultFrame = returnFrame_default
                print(f'currentFrame is {currentFrame}')
                print(f'defaultFrame is {defaultFrame}')
            
            currentFrame = cv2.resize(currentFrame, (int(1920),int(1080)))
            
            # defaultFrame = cv2.resize(currentFrame, int(1920),int(1080))
            
            currentFrame = Image.fromarray(cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB))
            
            # defaultFrame = Image.fromarray(cv2.cvtColor(defaultFrame, cv2.COLOR_BGR2RGB))
            
            current_image_tk = ImageTk.PhotoImage(image=currentFrame)
            compare_canvas.itemconfig(compare_canvas_image,image = current_image_tk)
            compare_canvas.image = current_image_tk
            print('process done')
            compare_ready = True
        # compare_interface.after(100, compare_update_canvas)
    
    
    # update canvas thread
    
    
    
    compare_thread1 = threading.Thread(target= compare)
    compare_thread1.start()
    
    compare_thread2 = threading.Thread(target= compare_update_canvas)
    compare_thread2.start()
    print('\nthread1 started\n')
    
    # compare_update_canvas()
    compare_interface.mainloop()
    
    
def compare():
    global default_image,compare_canvas, compare_canvas_image, compare_interface, returnFrame_current, returnFrame_default, compare_ready
    while not compare_threadKill.is_set():
        if not compare_threadPause.is_set():
            print('******************')
            print('entered internal comparison')
            print('******************')
            
            # get current frame
            with camLock:
                if stat:
                    current_frame = pic.copy()
                else:
                    tk.messagebox.showinfo(title= "warning", message= "something is wrong at line 224")

            grayDef = cv2.cvtColor(default_image, cv2.COLOR_BGR2GRAY)
            grayComp = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

            (score,diff) = compare_ssim(grayDef,grayComp,full=True)
            diff = (diff*255).astype("uint8")
            print(f"SSIM comparison score : {score}")
            # threshold the difference image, followed by finding contours to
            # obtain the regions of the two input images that differ
            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # loop over the contours
            for c in cnts:
                # compute the bounding box of the contour and then draw the
                # bounding box on both input images to represent where the two
                # images differ
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(default_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            with compareLock:
                global returnFrame_current, returnFrame_default
                returnFrame_current = current_frame
                returnFrame_default = default_image
                    
                    # change this if return value is nonetype
            # returnFrame_default = returnFrame_default
            # returnFrame_current = returnFrame_current
            time.sleep(1)
            print('compare done')
            compare_ready = True

    
    
    
def exitter():
    threadKill.set()
    print('threadkill set')
    exit()

__init__()

exitter()
