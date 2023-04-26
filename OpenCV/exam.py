import cv2
import numpy as np

def mskCombine(downTotal):
    setmskComb = len(downTotal) - 1
    counter = 0
    savor = {}
    
    while setmskComb > 0:
        if counter != len(downTotal):
            if counter == 0:
                savor[counter] = cv2.bitwise_or(downTotal[setmskComb], downTotal[setmskComb-1])
                
            else:
                savor[counter] = cv2.bitwise_or(savor[counter-1],downTotal[setmskComb-1])
                
        counter += 1
        setmskComb -= 1

    finalCombined = savor[counter-1]

array = (np.array([162,100,100]),np.array([104,50,100]),np.array([33,50,50]))
mskCombine(array)
