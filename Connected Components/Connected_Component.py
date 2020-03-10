import cv2 as cv

##################
#Common Tweaks
IMAGE_NAME = "readImage.jpg"
THRESH_VAL= 127
OUTPUT_IMAGE = "output.jpg"
#################

def isSurrounded(image, i, j):

    if(image[i+1][j+1] == 255 and image[i-1][j-1] ==255
    and image[i][j-1] == 255 and image[i+1][j] == 255
    and image[i][j+1]==255 and image[i-1][j+1] == 255
    and image[i+1][j-1] == 255 and image[i-1][j] ==255):
        
        return True

def my_Edge_Detector(image):
    
    rows, cols = image.shape
    img = image.copy()
    
    for i in range(0, rows-1):
        for j in range(0, cols-1):
            if(image[i][j] == 255):
                if(not isSurrounded(image, i, j)):  #Edge Found
                    img[i,j] = 255;
                else:
                    img[i,j] = 0;
    return img

image = cv.imread("opencv.png", 0)
ret,image = cv.threshold(image,THRESH_VAL,255,cv.THRESH_BINARY)
output = my_Edge_Detector(image)
cv.imwrite(OUTPUT_IMAGE, output)
