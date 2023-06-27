# requires to install
# pip install --upgrade scikit-image
# pip install --upgrade imutils

import cv2
from skimage.metrics import structural_similarity as compare_ssim
import tkinter as tk
import argparse
import imutils
import threading

camLock = threading.Lock()
threadKill = threading.Event()

# image variables
defImage = None
compImage = None

# interface
cam = cv2.VideoCapture(0)


def __init__():
    thread1 = threading.Thread(target=camWork)
    thread1.start()
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
    camInterface = tk.Tk()
    camInterface.title('Detection Interface')
    camInterface.geometry('400x530')
    camInterface.resizable(True, True)
    
    def def_capture():
        global defImage ,captured
        print('entered capture')
        with camLock:
            if stat:
                captured = pic.copy()
                defImage = captured.copy()
            else:
                print('warning! cam not avail')
    
    button_capture = tk.Button(camInterface, text="capture", command=def_capture) 
    button_capture.place(x=30,y=100)
    button_compare = tk.Button(camInterface, text="compare", command=comp_capture)
    button_compare.place(x= 90, y=100)
    
    camInterface.mainloop()
    
def comp_capture():
    global comp_capture
    print('entered compare capture')
    
    with camLock:
        if stat:
            print('captured as comparison target')
            frame = pic.copy()
            comp_capture = frame.copy()
            compare()
        else:
            print('warning camera not avail, line 73')
            pass

def compare():
    global defImage, compImage
    # load the two input images
    imageDef = cv2.imread(defImage)
    imageComp = cv2.imread(compImage)
    
    
    # convert the images to grayscale
    grayDef = cv2.cvtColor(imageDef, cv2.COLOR_BGR2GRAY)
    grayComp = cv2.cvtColor(imageComp, cv2.COLOR_BGR2GRAY)
    
    (score,diff) = compare_ssim(grayDef,grayComp,full=True)
    diff = (diff*255).astype("uint8")
    print(f"SSIM comparison score : {score}")
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
    
__init__()
    
