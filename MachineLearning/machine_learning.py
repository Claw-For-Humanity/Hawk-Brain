# tensorflow object detection

import cv2
import uuid
import os
import time

labels = ["one", "two", "three"]

number_of_imgs = 5

img_path = os.path.join('Tensorflow','workspace','images','collectedimages')

if not os.path.exists(img_path):
    os.makedirs(img_path)


for label in labels:
    path = os.path.join(img_path, label)

