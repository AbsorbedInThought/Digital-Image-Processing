import cv2
import numpy as np

#Applies a Red Color Filter to the Image

img = cv2.imread("readImage.jpg", 1)

imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

filter1 = cv2.inRange(imgHSV, (170, 150, 0), (180, 255,255))

filter2 = cv2.inRange(imgHSV, (0,150,0), (10, 255, 255))

mask = cv2.bitwise_or(filter1, filter2)

output = cv2.bitwise_and(img,img, mask=mask)

#Shows Input and Output Image Side by Side
myoutput = np.concatenate((img, output), axis = 1)

cv2.imwrite("myoutput.jpg", myoutput)
