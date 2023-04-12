import cv2
import numpy as np
import math
import struct
import serial
import serial.tools.list_ports
import tkinter as tk


def interface():
    window = tk.Tk()
    window.title("Project Claw For Humanity Port Selector")
    window.geometry("600x240")
    window.resizable(True,True)
    ComLable = tk.Label(window, text='Enter com port', font=('Arial', 15))
    ComLable.place(x=250,y=0)
    ComEnt = tk.Entry(window)
    ComEnt.place(x= 250, y= 100)
    CamPortLabel = tk.Label(window, text='Enter Camera Port // Default is 0', font=('Arial',15))
    CamPortLabel.place(x=250, y=320)
    btn = tk.Button(window, text='Next')
    btn.config(command=__startPort__(ComEnt))
    btn.place(x= 250, y= 300)
    window.mainloop()
    
def colourInterface():
    ColourWindow = tk.Tk()
    ColourWindow.title("Project Claw For Humanity Main")
    ColourWindow.geometry("1000x800")
    ColourWindow.resizable(True,True)
    # colours and buttons
    redBtn = tk.Button(ColourWindow, text='red')
    redBtn.place(x= 100, y= 100)
    bluBtn = tk.Button(ColourWindow, text='blue')
    bluBtn.place(x= 200, y= 100)
    yelBtn = tk.Button(ColourWindow, text = 'green')
    yelBtn.place()
    

                        # camera work
# global variables for contour ***DO NOT CHANGE***
resolution = 1280,720
actual_redbox = None
actual_redbox = None

cameraAngle = 130
frontVid = None



def __initializeCam__(port):

    global frontVid
    global centerXY
    global resolution

    
    
    #catch Camera
    frontVid = cv2.VideoCapture(port)
    if frontVid.isOpened():
        print("[LOG] " + f'front vid // selected port is "{port}"')
    else:
        print(f'Check port -- Camera {port}')
        tk.messagebox.showinfo(title='Warnign', message='Check Your Camera Port')

        
    
    # set camera resolution
    # 640 * 380 or 1280 * 720
    frontVid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    frontVid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # camera size
    resolution = (frontVid.get(3),frontVid.get(4))
    
    # find center // x 590, x+w 690, y 410, y+h 310 (width and height is 50 pixels. Therefore, add and subtract 50)
    centerXY = resolution[0]/2-50, resolution[1]/2+50, 50, 50
    # calculated values
    # center x y x+w y+h
    # 590, 410, 690, 310 



                        # com work

# global variables for serial com
serialComPort = 3
serialInst = None # dont touch this

def __startPort__(COMPORT):
    global window
    window.destroy()
    print('entered startport')
    global serialComPort
    global serialInst

    serialInst = serial.Serial()
    serialInst.port = str(COMPORT)
    serialInst.open()
    if not serialInst.is_open:
        tk.messagebox.showinfo(title='Warnign', message='Check Your COM Port')
        return
    else:
        pass
    print('finished startport without problem')



# colour
# red = 1 // green = 2 // blue = 3
def sender(time):
    global serialInst
    data = time
    packed = data.encode()
    serialInst.write(packed)
    print(f'Packed data sent, sent data is {packed}')
    





                        # detection work

# global variables for detections
centerred = None
centerGreen = None
centerblue = None
red1 = (0,0,0,0)
green1 = (0,0,0,0)
blue1 = (0,0,0,0)
centerXY = (0,0,0,0)
greenerReturn = None
blueerReturn = None
redrReturn = None

# colour range
red_lower_colour = np.array([162,100,100])
red_upper_colour = np.array([185,255,255])

blue_lower_colour = np.array([104,50,100])
blue_upper_colour = np.array([126,255,255])

green_lower_colour = np.array([33,50,50])
green_upper_colour = np.array([40,255,255])

# actual sizes of things in mm
actual_redbox = 243,243
actual_bluecone = 210,330
actual_greenlight = 100,100



def _detect_(camera):  
    global combined_mask
    global result
    # video input
    read, standard = camera.read()

    bottomHsv = cv2.cvtColor(standard, cv2.COLOR_BGR2HSV)

    # make mask
    bottom_red_mask = cv2.inRange(bottomHsv, red_lower_colour, red_upper_colour)
    bottom_blue_mask = cv2.inRange(bottomHsv, blue_lower_colour, blue_upper_colour)
    bottom_green_mask = cv2.inRange(bottomHsv, green_lower_colour, green_upper_colour)

    # combine masks
    combined_mask = cv2.bitwise_or(bottom_red_mask,cv2.bitwise_or(bottom_blue_mask,bottom_green_mask))

    # create result
    result = cv2.bitwise_and(standard, standard, mask= combined_mask)

    # create videos dictionary
    videos = [result, combined_mask]    

    # draw boxes
    contours1, _1 = cv2.findContours(bottom_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours1:
        global red1
        global redReturn
        red1 = cv2.boundingRect(contour)
        # sender('red', red1)
        if red1[2]>90 and red1[3]>90:          
            centerred = (2*red1[0]+red1[2])//2, (2*red1[1]+red1[3])//2
            print('')
            for redVid in videos:
                cv2.rectangle(redVid,(red1[0],red1[1]),(red1[0]+red1[2],red1[1]+red1[3]),(172,0,179),2)
                cv2.circle(redVid, centerred, 1, (255,0,0) ,thickness=3)
                # sender('red')
                
    contours2, _2 = cv2.findContours(bottom_blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours2:
        global blue1
        global blueerReturn
        blue1 = cv2.boundingRect(contour)
        if blue1[2]>90 and blue1[3]>90:
            centerblue = (2*blue1[0]+blue1[2])//2, (2*blue1[1]+blue1[3])//2
            # sender('blue', blue1)
            for blueVid in videos:
                cv2.rectangle(blueVid,(blue1[0],blue1[1]),(blue1[0]+blue1[2],blue1[1] + blue1[3]),(0,255,255),2)
                cv2.circle(blueVid, centerblue, 1, (255,0,0) ,thickness=3)
                # sender('blue')
        

    contours3, _3 = cv2.findContours(bottom_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours3:
        global green1
        global greenerReturn
        green1 = cv2.boundingRect(contour)
        if green1[2]>90 and green1[3]>90:
            centerGreen = (2*green1[0]+green1[2])//2, (2*green1[1]+green1[3])//2
            # sender('green', green1)
            for greenVid in videos:
                cv2.rectangle(greenVid, (green1[0], green1[1]), (green1[0] + green1[2], green1[1] + green1[3]), (0, 255, 0), 2)
                cv2.circle(greenVid, centerGreen, 1, (255, 0, 0), thickness=3)
        else:
            greenerReturn = None

    # make a box at center
    for boxes in videos:
        cv2.rectangle(boxes,(590,410), (690,310), (0,0,255), 2) 
    
    # center pixel hsv value
    centerBottomHsv = bottomHsv[360,640]
    
    print(centerBottomHsv)
    # make a circle
    cv2.circle(result, (360,640) , 5, (255,0,0), 3)
    #print(colour)

    





                        # initialize / work
def __initialize__():
    print('cam port')
    __startPort__()
    print('startport done')
       
    
    print('initialize')
    __initializeCam__()
    print('initialize camera done')
    
    
    print('start working')
    __work__()
    print('work done')

    #release camera
    frontVid.release()
    cv2.destroyAllWindows()



def __work__():
    i = 0
    global frontVid
    global red_upper_colour
    global red_lower_colour
    global blue_upper_colour
    global blue_lower_colour
    global green_upper_colour
    global green_lower_colour
    global red1
    global green1
    global blue1
    global greenerReturn
    
    print('Ready to enter while loop')
    while(True):
        if(frontVid.isOpened()):
            _detect_(frontVid)
     
        

        # stop loop when q is pressed
        if cv2.waitKey(1) == ord('q'):
            print(f'loop happened {i} times')
            break
        i+=1
        # show video // result displays with colour // combined mask displays white and black
        cv2.imshow('result', result)
        cv2.imshow('combined mask', combined_mask)
        


# 1. detects location and send it to solenoid (motor is timed, )
# 2. movement time



# start from here
# __initialize__()

interface()


# color selection

# json file -> saves settings
