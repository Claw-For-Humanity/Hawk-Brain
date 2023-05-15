import struct
import serial
import tkinter as tk
import time
import threading



serialInst = serial.Serial(port='/dev/cu.usbmodem1101', baudrate= 9600)

killFlag = threading.Event()

incomingState = False
    
def log(widget, message, level = 'INFO'):
    tag = level.upper()
    widget.insert(tk.END, message + "\n", tag)

def send(data):
    global serialInst
    print(f'\n{data.encode()} is written\n')
    serialInst.write(f"{data}".encode())
    
    
receiveLock = threading.Lock()

def receive(serialInst):
    print('receive entered')
    n = 0
    while True:
        
        if type(serialInst) != type(None):
            if serialInst.in_waiting > 0:
                data = serialInst.readline().decode().strip() # Read data from the serial port
                print("Received data:", data)
                decoded = data
                with receiveLock:
                    global decodedData, incomingState
                    if not decoded == None:
                        n+=1
                        incomingState = True
                        decodedData = decoded
                    else:
                        incomingState = False
                        decodedData = None
                n+=1
                
def update_gui():
    with receiveLock:
        global decodedData, incomingState
        if incomingState == True:
            log(text_widget, f'incoming bytes from arduino {decodedData}')
        elif incomingState == False: 
            log(text_widget, f'waiting for incoming bytes from arduino')

        global loggingbox
        loggingbox.after(1000, update_gui) # schedule update_gui to be called again in 1 second


def logging():
    global loggingbox, text_widget
    loggingbox = tk.Tk()
    loggingbox.title('logger')
    print(loggingbox.state)

    loggingbox.geometry("1000x1000")
    loggingbox.resizable(True,True)
    text_widget = tk.Text(loggingbox, height=20, width=80)
    text_widget.pack()
    enter_widget = tk.Entry(loggingbox, width= 18)
    nxt_btn = tk.Button(loggingbox, text='send', command=lambda: send(enter_widget.get()), width= 2)
    nxt_btn.place(x=20, y= 90)
    enter_widget.pack()
    
    
    
    log(text_widget, "waiting for incoming bytes...")

    print('thread about to start')
    
    thread2 = threading.Thread(target=receive, args=(serialInst,))
    thread2.start()
    print(f'thread started and thread state is {thread2.is_alive}')
    print('about to enter update gui')
    loggingbox.after(1000, update_gui)
    loggingbox.mainloop()


if serialInst.is_open:
    logging()
    
    killFlag.set()
    print(f'killflag is set, killflag status is {killFlag.is_set}')
    exit()
else:
    print('error connection')
    exit()
    

