import cv2
import uuid
import os
import time
# import keyboard # usage of keyboard requires admin previliges (maybe windows may be different)
import sys
import ctypes


collectType = ['one', 'two']
number_img = 5
imgPath =os.path.join(os.getcwd(),'Tensorflow', 'workspace', 'images', 'collectedData')
camState = False
vid = cv2.VideoCapture(0)
frames = None
currentIMG = 0
currentType = 0
currentIMG = 0
currentType = 0

print(imgPath)

def sourceCollector():
    if not os.path.exists(imgPath):
        # os.makedirs(imgPath)
        print(f'{imgPath} / new directory made')
    else:
        print(f'directory already exists -- {imgPath}')
        pass

    for type in collectType:
        path = os.path.join(imgPath, type)

        if not os.path.exists(path):
            os.makedirs(path)
            print('inner path updated')
            print(f'inner path is {path}')

    print('\n\nfolder check pass')
    print('entering photo take')


    displayCam()
    labeler()
    

    

def displayCam():
    
    maxType = len(collectType)
    maxImg = number_img
    
    global vid, camState, frames
    while True:
        ret, std = vid.read()
        
        if not ret:
            break
        
        cv2.imshow('camera', std)
        
        def photoTake():
            global currentIMG, currentType, currentIMG, currentType
            if currentIMG == maxImg + 1:
                currentIMG = 0
                currentType += 1
                
            if currentType == maxType:
                print('done')
                exit()

            # copy frame to the picture 
            picture = std.copy()
            
            # print out collecting image
            print(f'collecting image for {collectType[currentType]}')
            # sleep for 5 seconds
            time.sleep(5)
            print(f'collecting image number {currentIMG}')
            imgname = os.path.join(imgPath, collectType[currentType], collectType[currentType] + '.' + f'{str(uuid.uuid1())}.jpg')
            cv2.imwrite(imgname, picture)
            print(f'written @ {imgname}')
            
            currentIMG += 1
         
        photoTake()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def labeler():
    labele_path =  os.path.join(os.getcwd(),'Tensorflow', 'labelimg')
    print(labele_path)
    if not os.path.exists(labele_path):
        # make directory
        os.makedirs(labele_path)
        


sourceCollector()



