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


compImgLock = threading.Lock()
camLock = threading.Lock()
threadKill = threading.Event()

# image variables
defImage = None
compImage = None

goodbyeWindow = False
defCaptureStat = False
initWindowKilled = False

frame = None
holdFrame = None


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
    
    # create window
    captureWindow = tk.Tk()
    captureWindow.title('capture window')
    captureWindow.geometry("2000x1300")
    
    # create canvas
    canvas = tk.Canvas(captureWindow, width=1920, height=1080)
    canvas.place(x=30,y=60)
    canvas_image = canvas.create_image(0, 50, anchor=tk.NW)
    print('canvas created') 

    #capture button
    captureBtn = tk.Button(captureWindow,text="capture", command= captureDef)
    captureBtn.place(x=30, y=30)    
    
    # update the video in a loop
    
    def update_canvas():
        

        print('updating canvas on new window')
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
        
        if goodbyeWindow:
            captureWindow.destroy()
        
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
            defImage = pic.copy()
        else:
            print('check cam status')
            pass
    
    captureWindow.mainloop()
        
    
def init_compare():
    global captureWindow, defCaptureStat, goodbyeWindow
    
    goodbyeWindow = True
    
    print('\n\ninitating comparing process\n\n')
    
    thread1 = threading.Thread(target=get_comp_img)
    thread1.start()
    
    print('**thread1 started**')
    
    thread2 = threading.Thread(target=compare)
    thread2.start()
    
    print('**thread2 started**')
    print('init compare started')

    i = 0
    
    while not threadKill.is_set():
        i +=1

def get_comp_img():
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
    global frame, compImage
    
    compareTK = tk.Tk()
    compareTK.title('compare engine v1.0')
    compareTK.geometry('1200x1000')
    compareTK.resizable(True,True)
    
    canvas1 = tk.Canvas(compareTK)
    canvas1.place(x=30, y=30)
    canvas1_image = canvas1.create_image(0,50,anchor=tk.NW)
    print('canvas created')
    
    def update_canvas(image):
        frame1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame1 = cv2.resize(frame, (int(1920),int(1080)))
        
        img1 = Image.fromarray(frame1)
        imgtk1 = ImageTk.PhotoImage(image=img1)
        canvas1.itemconfig(canvas1_image, image= imgtk1)
        canvas1.image = imgtk1
        print('done')
        compareTK.update()
    
    while not threadKill.is_set():
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
        
        
        
        compareTK.after(10,func=lambda:update_canvas(imageComp))
        print('line 230 done')
        print('line 233 done')
        compareTK.mainloop()
        
__init__()

threadKill.set()
print('thread kill set')
exit()