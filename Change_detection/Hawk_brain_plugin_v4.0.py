
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import tkinter as tk
import argparse
import imutils
import threading
from PIL import Image, ImageTk
import time
from tkinter import messagebox


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
