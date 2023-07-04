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

# threads
compImgLock = threading.Lock()
camLock = threading.Lock()
threadKill = threading.Event()
threadPause = threading.Event()



# image variables
defImage = None
compImage = None
compare_ready = False

goodbyeWindow = False
defCaptureStat = False
initWindowKilled = False

frame = None
holdFrame = None

# trace
count_compare = 0
count_updateWindow = 0
count_captureUpdate = 0
count_initComp = 0


# interface
cam = cv2.VideoCapture(0)


def __init__():
    thread1 = threading.Thread(target=camWork)
    thread1.start()
    print('cam capturing initiated')
    interface_cam()

def camWork ():
    while not threadKill.is_set():
        ret, frame = cam.read()
        if ret:
            with camLock:
                global pic,stat
                pic = frame.copy()
                stat = ret
        else:
            print('cam not ready!')
            pass

def interface_cam():
    global camInterface 
    camInterface = tk.Tk()
    camInterface.title('Detection Interface')
    camInterface.geometry('400x530')
    camInterface.resizable(True, True)            
    
    button_initiate = tk.Button(camInterface, text= 'start', command=CaptureInterface)
    button_initiate.place(x= 30, y= 100)
    
    camInterface.mainloop()

captureWindow = None
def CaptureInterface():
    global defCaptureStat,captureWindow,initWindowKilled
    print('entered capture default frame')
    if not initWindowKilled:
        camInterface.destroy()
        initWindowKilled = True
        print('destroyed camInterface')
    
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
            with camLock:
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
                init_compare()
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
        resetBtn = tk.Button(captureWindow, text="reset", command=reset)
        resetBtn.place(x = 150, y= 30)

        with camLock:
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

def reset():
    print('reset entered')
    captureWindow.destroy()
    CaptureInterface()

def killwindow():
    global goodbyeWindow
    while not threadKill.is_set():
        goodbyeWindow = True
        print(f'goodbyewindow is {goodbyeWindow}')

def init_compare():
    global captureWindow, defCaptureStat, goodbyeWindow, count_initComp
    
    print('\n\ninitating comparing process\n\n')
    thread1 = threading.Thread(target=get_comp_img)
    # thread1.start()
    
    print('**thread1 started**')
    
    thread2 = threading.Thread(target=compare)
    # thread2.start()
    
    print('**thread2 started**')
    print('init compare started')

    
    while not threadKill.is_set():
        print('working...')
        time.sleep(1)
        count_initComp += 1

def get_comp_img():
    global count_captureUpdate
    while not threadKill.is_set():
        with camLock:
            if stat:
                tempFrame = pic.copy()
        with compImgLock:
            global holdFrame
            holdFrame = tempFrame.copy()
        
        count_captureUpdate += 1

def compare():
    print('entered compare ')
    
    global frame, compImage
    
    compareTK = tk.Toplevel()
    compareTK.title('compare engine v1.0')
    compareTK.geometry('1200x1000')
    compareTK.resizable(True,True)
    print('line 196 -- window is created')
    
    canvas1 = tk.Canvas(compareTK)
    canvas1.place(x=30, y=30)
    canvas1_image = canvas1.create_image(0,50,anchor=tk.NW)
    print('line 201 -- canvas created')
    
    def update_canvas(image):
        print('entered update_canvas')
        global count_updateWindow
        frame1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame1 = cv2.resize(frame1, (int(1920),int(1080)))
        
        img1 = Image.fromarray(frame1)
        imgtk1 = ImageTk.PhotoImage(image=img1)
        canvas1.itemconfig(canvas1_image, image= imgtk1)
        canvas1.image = imgtk1
        print('line 211 update canvas done')
        
        count_updateWindow += 1
        
        compareTK.after(100,internal_comparison)
    
    def internal_comparison():
        global count_compare
        print('******************')
        print('entered internal comparison')
        print(f'[LOG] count compare happened {count_compare} times')
        print('******************')
                
        with compImgLock:
            if type(holdFrame) != type(None):
                imageComp = holdFrame.copy()
            else:
                print(f'warning check holdFrame type || {type(holdFrame)}')
          
        if type(imageComp) == type(None):
            print('warning! camera frame == None')
            print(f'type of frame is {type(imageComp)}')
            return
    
        # print(f'\n\nimageDef is {imageDef}\n\ntype of imageDef is {type(imageDef)}\n\n')
        print(f'\n\nimage compare is {imageComp}\n\ntype of image compare is {type(imageComp)}\n\n')
        
        # convert the images to grayscale
        grayDef = cv2.cvtColor(defImage, cv2.COLOR_BGR2GRAY)
        grayComp = cv2.cvtColor(imageComp, cv2.COLOR_BGR2GRAY)
        
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
            cv2.rectangle(defImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageComp, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # imageComp = Image.fromarray(cv2.cvtColor(imageComp, cv2.COLOR_BGR2RGB))
        # imageDef = Image.fromarray(cv2.cvtColor(imageDef, cv2.COLOR_BGR2RGB))
        
        count_compare += 1
        print('line 230 done')
        print('line 233 done')
        update_canvas(imageComp)
        
    internal_comparison()
        
__init__()


if compare_ready:
    print('\n\nentering sleep\n\n')
    time.sleep(10)
    print(f'compare ready : {compare_ready}')


threadKill.set()
print('thread kill set')

print(f'[LOG] init_comparison happened {count_initComp} times')
print(f'[LOG] get_comp_img happened {count_captureUpdate}times')
print(f'[LOG] update window happened {count_updateWindow} times')
print(f'[LOG] line 224 internal comparison happened {count_compare} times')


exit()