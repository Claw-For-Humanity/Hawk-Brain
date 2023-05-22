import cv2
import uuid
import os
import time
import keyboard # usage of keyboard requires admin previliges (maybe windows may be different)
import sys

collectType = ['one', 'two']
number_img = 5
imgPath = os.path.join('Tensorflow', 'workspace', 'images', 'collectedData')
camState = False
vid = cv2.VideoCapture(0)
frames = None
currentIMG = 0
currentType = 0
currentIMG = 0
currentType = 0
        

# for windows
# import ctypes
# import sys

# def run_with_admin():
#     if ctypes.windll.shell32.IsUserAnAdmin():
#         # User already has administrative privileges
#         print("Running with administrative privileges.")
#     else:
#         # Prompt user to elevate privileges
#         params = " ".join([sys.executable] + sys.argv)
#         ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

# # Call the function to check and prompt for administrative privileges
# run_with_admin()



# for mac

def run_with_admin():
    if os.getuid() == 0:
        # User already has administrative privileges
        print("Running with administrative privileges.")
    else:
        # Prompt user to elevate privileges
        script_path = os.path.abspath(sys.argv[0])
        os.system(f"osascript -e 'do shell script \"{script_path}\" with administrator privileges'")

# Call the function to check and prompt for administrative privileges
run_with_admin()



def sourceCollector():
    if not os.path.exists(imgPath):
        os.makedirs(imgPath)
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


    # displayCam()
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
        
        def takePic():
            global currentIMG, currentType, currentIMG, currentType
            if currentIMG == maxImg + 1:
                currentIMG = 0
                currentType += 1
                
            if currentType == maxType + 1:
                print('done')

            # copy frame to the picture 
            picture = std.copy()
            
            # print out collecting image
            print(f'collecting image for {collectType[currentType]}')
            # sleep for 5 seconds
            time.sleep(5)
            print(f'collecting image number {currentIMG}')
            imgname = os.path.join(imgPath, collectType[currentType], collectType[currentType] + '.' + f'{str(uuid.uuid1())}.jpg')
            cv2.imwrite(imgname, picture)
            
            currentIMG += 1
        
        
        takePic()       


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def labeler():
    labele_path = os.path.join('tensorflow', 'labelling')
    if not os.path.exists(labele_path):
        os.makedirs(labele_path)


sourceCollector()



