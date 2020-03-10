import cv2 as cv

##################
#Common Tweaks
NEIGHBORS = 8
THRESH_VAL = 127
IMAGE_NAME = "readImage.jpg"
#################

#Selects connected components of an image within a specific height threshold

img = cv.imread(IMAGE_NAME, 0)
ret,image = cv.threshold(img,THRESH_VAL,255,cv.THRESH_BINARY)
rows, cols = image.shape

return_list = cv.connectedComponentsWithStats(image, NEIGHBORS, cv.CV_32S)

objects = return_list[1]
height = return_list[2][:,3]
height = height > rows/2

for i in range(0, rows):
    for j in range(0, cols):
        if(height[objects[i][j]] == True and objects[i][j] != 0):
            objects[i][j] = 255
        else:
            objects[i][j] = 0
        
cv.imwrite("output.jpg", objects)
