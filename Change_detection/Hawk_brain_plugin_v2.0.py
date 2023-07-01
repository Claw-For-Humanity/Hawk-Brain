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

camLock = threading.Lock()
threadKill = threading.Event()

# image variables
defImage = None
compImage = None


goodbyeWindow = False
defCaptureStat = False
initWindowKilled = False

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

def CaptureInterface():
    global defCaptureStat,captureWindow,initWindowKilled
    
    print('entered capture default frame')
    if not initWindowKilled:
       camInterface.destroy()
       initWindowKilled = True
    print('destroyed camInterface')
    
    captureWindow = tk.Tk()
    captureWindow.title('capture window')
    captureWindow.geometry("2000x1300")
    
    
    
    canvas = tk.Canvas(captureWindow, width=1920, height=1080)
    canvas.place(x=30,y=60)
    
    
    captureBtn = tk.Button(captureWindow,text="capture", command= captureDef)
    captureBtn.place(x=30, y=30)
    
    canvas_image = canvas.create_image(0, 50, anchor=tk.NW)
    print('canvas created') 

    
    # update the video in a loop
    def update_canvas():
        print('entered update canvas')
        while defCaptureStat:
            if goodbyeWindow == True:
                captureWindow.destroy()
                print('wait')
                time.sleep(3)
            else:
                captureWindow.after(100, update_canvas)
        
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
        
    update_canvas()

def reset():
    print('reset entered')
    captureWindow.destroy()
    CaptureInterface()

def captureDef():    
    global defImage, defCaptureStat
    print('capturing default frame')
    
    defCaptureStat = True
    
    nextBtn = tk.Button(captureWindow, text="next", command=init_compare)
    nextBtn.place(x=80, y=30)
    resetBtn = tk.Button(captureWindow, text="reset", command=reset)
    resetBtn.place(x = 150, y= 30)
    
    with camLock:
        if stat:
            print('capturing...')
            defImage = pic.copy()
            # print(f'captured / defImage is {defImage}')
        else:
            print('warning || captureDef failed due to camera errors')
            pass
    captureWindow.mainloop()
        
    
def init_compare():
    global captureWindow, defCaptureStat, goodbyeWindow
    # goodbyeWindow = True
    # captureWindow.destroy()
    print('\n\nabout to initiate init_compare\n\n')
    
    time.sleep(5)
    
    thread1 = threading.Thread(target=get_comp_img)
    thread1.start()
    thread2 = threading.Thread(target=compare)
    thread2.start()
    print('init compare started')
    i = 0
    while not threadKill.is_set():
        i +=1

frame = None
holdFrame = None

compImgLock = threading.Lock()


def get_comp_img():
    global holdFrame
    while not threadKill.is_set():
        with camLock:
            if stat:
                tempFrame = pic.copy()
        
        # print(f'tempframe is {tempFrame}')
        
        with compImgLock:
            global holdFrame
            holdFrame = tempFrame.copy()
            # print(f'hold frame is {holdFrame}')

def compare():
    global frame, defImage, compImage
    imageDef = defImage
    
    compareTK = tk.Tk()
    compareTK.title('compare engine v1.0')
    compareTK.geometry('1200x1000')
    compareTK.resizable(True,True)
    
    canvas = tk.Canvas(compareTK)
    canvas.place(x=30, y=30)
    canvas_image = canvas.create_image(0,50,anchor=tk.NW)
    print('canvas created')
    
    def update_canvas(image):
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (int(1920),int(1080)))
        
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.itemconfig(canvas_image, image= imgtk)
        canvas.image = imgtk
        print('done')
        compareTK.update()
    
    while True:
        print('******************')
        print('entered comapare')
        print('******************')
                
        with compImgLock:
            if type(holdFrame) != type(None):
                frame = holdFrame.copy()
            else:
                print(f'warning check holdFrame type || {type(holdFrame)}')
        
        
        if type(frame) == type(None):
            print('warning! camera frame == None')
            print(f'type of frame is {type(frame)}')
            return
        else:
            pass
        
    
        
        imageComp = frame
    
        # print(f'\n\nimageDef is {imageDef}\n\ntype of imageDef is {type(imageDef)}\n\n')
        print(f'\n\nimage compare is {imageComp}\n\ntype of image compare is {type(imageComp)}\n\n')
        
        # convert the images to grayscale
        grayDef = cv2.cvtColor(imageDef, cv2.COLOR_BGR2GRAY)
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
            cv2.rectangle(imageDef, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageComp, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # imageComp = Image.fromarray(cv2.cvtColor(imageComp, cv2.COLOR_BGR2RGB))
        # imageDef = Image.fromarray(cv2.cvtColor(imageDef, cv2.COLOR_BGR2RGB))
        
        
        
        compareTK.after(10,func=lambda:update_canvas(imageComp))
        print('line 230 done')
        print('line 233 done')
        compareTK.mainloop()
        
__init__()

threadKill.set()
print('thread kill set')
exit()