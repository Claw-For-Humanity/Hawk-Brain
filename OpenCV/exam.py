import cv2
import numpy as np

def mskCombine(downTotal):
    setmskComb = len(downTotal) - 1
    counter = 0
    trace = 0
    savor = {}
    while setmskComb > 0:
        trace += 1
        print(f'trace; while loop happened {trace}')
        print(f'setmskComb is {setmskComb}')
        print(f'counter is {counter}')
        
        if counter != len(downTotal):
            if counter == 0:
                savor[counter] = cv2.bitwise_or(downTotal[setmskComb], downTotal[setmskComb-1])
                print(f'counter is 0 {savor[counter]}\n \n')
            else:
                print(f'counter is {counter} and setmskComb is {setmskComb}')
                savor[counter] = cv2.bitwise_or(savor[counter-1],downTotal[setmskComb-1])
                print(f'savor is {savor[counter]}\n \n')
                
        counter += 1
        setmskComb -= 1

    finalCombined = savor[counter-1]
    print(f"final combined mask is {finalCombined}")

array = (np.array([162,100,100]),np.array([104,50,100]),np.array([33,50,50]))
mskCombine(array)
