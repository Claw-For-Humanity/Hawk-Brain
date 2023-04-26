import tkinter as tk
from tkinter import messagebox
import cv2
import serial.tools.list_ports
import serial
from PIL import Image, ImageTk
import subprocess
import threading
import time
import numpy as np

def __initiate__():
    # create variables
    global window
    
        # create window using tkinter
    window = tk.Tk()
        # title of the window
    window.title("Project Claw For Humanity Port Selector")
        # resolution of the window
    window.geometry("600x240")
        # whether or not it is resizable
    window.resizable(True,True)
    
        # options for baudrate
    baudRates = [300,1200,2400,9600,10417,19200,57600,115200]
        
        # default x location for camera entry
    ax = 30 
        # default y location for camera entry
    ay =  150 
        # default location for camera entry explanation
    ayl = 130 
    
        # Comport selection list
    comList_val = tk.StringVar(window, "Com Port")
    comList_val.set("Com Port")
    ComLable = tk.Label(window, text='Select Communication Port', font=('Arial', 15))
    ComLable.place(x=ax,y=20)
    
        # baud rate selection list
    baud_val = tk.StringVar(window,"Baud Rate")
    baud_val.set("Baud Rate")
    baudLable = tk.Label(window, text="Select Baud Rate", font=('Arial', 15))  
    baudLable.place(x= ax, y= 80)  
    
        # cam port selection list   
