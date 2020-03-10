import cv2
import numpy as np


def myInRange(img, HueLow, SatLow, valueLow, HueHigh, SatHigh, valueHigh):

    rows, cols, channels = img.shape

    flag = 1
    i = 0
    while(i < rows):
        j = 0
        while(j < cols):
            if(img[i][j][0] > HueLow and img[i][j][0] < HueHigh):
                if(img[i][j][1] > SatLow and img[i][j][1] < SatHigh):
                    if(img[i][j][2] > valueLow and img[i][j][2] < valueHigh):
                        img[i][j] = 255
                        flag = 0
                        
            if(flag == 1):
                img[i][j] = 0
                
            j=j+1
            flag = 1
            
        i=i+1
    return img
        
img = cv2.imread("readImage.jpg", 1)

#image, HueLow, SatLow, valueLow, HueHigh, SatHigh, valueHigh
output = myInRange(img, 0, 0, 0, 10, 255,255)

cv2.imwrite("outputImage.jpg", output)
