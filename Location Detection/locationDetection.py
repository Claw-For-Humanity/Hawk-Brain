import cv2
import numpy as np
import math
import struct
import threading




                        # camera work
# global variables for contour ***DO NOT CHANGE***
resolution = 1280,720
actual_redbox = None
actual_redbox = None
frontCamPort = 0
cameraAngle = 130
frontVid = None
threadKill = threading.Event()


def __initializeCam__():
    global frontCamPort
    global frontVid
    global centerXY
    global resolution

    #catch Camera
    frontVid = cv2.VideoCapture(frontCamPort)
    if frontVid.isOpened():
        print("[LOG] " + f'front vid // selected port is "{frontCamPort}"')
        
    
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



# colour
# red = 1 // green = 2 // blue = 
def sender(colour):
    print(colour)
    global serialInst
    packed = struct.pack('>' + 'f'*len(colour), *colour)
    # serialInst.write(packed)
    print(packed)
    serialInst.write()





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
selectedColour = {'red': False, 'blue': False}

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

objectRed = None
objectBlue = None

def _detect_(camera):  
    global thread1, combined_mask, result
    # video input
    read, standard = camera.read()

    bottomHsv = cv2.cvtColor(standard, cv2.COLOR_BGR2HSV)

    # make mask
    bottom_red_mask = cv2.inRange(bottomHsv, red_lower_colour, red_upper_colour)
    bottom_blue_mask = cv2.inRange(bottomHsv, blue_lower_colour, blue_upper_colour)
    
    # combine masks
    combined_mask = cv2.bitwise_or(bottom_red_mask,bottom_blue_mask)

    # create result
    result = cv2.bitwise_and(standard, standard)

    # create videos dictionary
    videos = [result, combined_mask]    

    # draw boxes
    contours1, _1 = cv2.findContours(bottom_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours1:
        global red1, redrReturn, objectRed
        red1 = cv2.boundingRect(contour)
        rx, ry, rw, rh = red1
        # sender('red', red1)
        if red1[2]>90 and red1[3]>90:          
            centerred = (2*red1[0]+red1[2])//2, (2*red1[1]+red1[3])//2
            print('')
            for redVid in videos:
                if selectedColour['red'] == True:
                    cv2.rectangle(redVid,(red1[0],red1[1]),(red1[0]+red1[2],red1[1]+red1[3]),(172,0,179),2)
                    cv2.circle(redVid, centerred, 1, (255,0,0) ,thickness=3)
                    objectRed = ((rx+rw)/2,(ry+rh)/2)
                else:
                    objectRed = None
                
    contours2, _2 = cv2.findContours(bottom_blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours2:
        global blue1, blueerReturn, objectBlue
        blue1 = cv2.boundingRect(contour)
        bx, by, bw, bh = blue1
        if blue1[2]>90 and blue1[3]>90:
            centerblue = (2*blue1[0]+blue1[2])//2, (2*blue1[1]+blue1[3])//2
            for blueVid in videos:
                if selectedColour['blue'] == True:
                    cv2.rectangle(blueVid,(blue1[0],blue1[1]),(blue1[0]+blue1[2],blue1[1] + blue1[3]),(0,255,255),2)
                    cv2.circle(blueVid, centerblue, 1, (255,0,0) ,thickness=3)
                    objectBlue = ((bx+bw)/2, (by+bh)/2)
                else:
                    objectBlue = None
        
    objectX = 700
    objectY = 0
    objectW = 200
    objectH = 720 
    
    
    objectPts = np.array([(objectX,objectY),(objectX+objectW, objectY),(objectX+objectW,objectY+objectH),(objectX,objectY+objectH)])
    
    def checker():
        while not threadKill.is_set():
            if type(objectBlue) != type(None):
                if cv2.pointPolygonTest(objectPts, objectRed, False) < 0:
                    blueState = False
                else:
                    blueState = True
            elif type(objectBlue) == type(None):
                print('type none blue')
            else: 
                print('not checking blue')
            
            if type(objectRed) != type(None):
                    if cv2.pointPolygonTest(objectPts, objectRed, False) < 0:
                        redState = False
                    else:
                        redState = True  
            elif type(objectRed) == type(None):
                print('type none red')
            else:
                print('not checking red')
                
    thread1 = threading.Thread(target= checker) 
    thread1.start()                       
                        
    # make a box at center
    for boxes in videos:
        cv2.rectangle(boxes,(590,410), (690,310), (0,0,255), 2) 
                            # x, y , x+w, y+h
    # target area box
    cv2.rectangle(result, (700,0), (900,720),(0,255,0),3)
    
    # center circle
    cv2.circle(result, (800,360),5, (255,0,0), 3)
    
    # center pixel hsv value
    centerBottomHsv = bottomHsv[640,360]
    
    print(centerBottomHsv)
    # make a circle
    cv2.circle(result, (360,640) , 5, (255,0,0), 3)
    #print(colour)

    

                        # initialize / work
def __initialize__():
    print('cam port')
    # __startPort__()
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
        # cv2.imshow(' ')
        


# 1. detects location and send it to solenoid (motor is timed, )
# 2. movement time



# start from here
__initialize__()
threadKill.set()
if thread1 is not None:
    thread1.join()
    exit()
    


# color selection

# json file -> saves settings
