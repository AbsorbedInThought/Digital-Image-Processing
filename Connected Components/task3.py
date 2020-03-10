# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 21:50:30 2019

@author: Taha
"""

import cv2 as cv

##################
#Common Tweaks
NEIGHBORS = 8
THRESH_VAL = 127
IMAGE_NAME = "circuit.png"
#################

img = cv.imread(IMAGE_NAME, 0)
ret,image = cv.threshold(img,THRESH_VAL,255,cv.THRESH_BINARY)
rows, cols = image.shape

return_list = cv.connectedComponentsWithStats(image, NEIGHBORS, cv.CV_32S)

no_of_objects = return_list[0]
objects = return_list[1]

color_shift = int(255/no_of_objects)
color_list = [0]*no_of_objects

for i in range(0, no_of_objects):
    color_list[i] = i*color_shift
    
    
for i in range(0, rows):
    for j in range(0, cols):
            color_value = color_list[objects[i][j]]
            objects[i][j] = color_value
        
cv.imwrite("output.png", objects)
