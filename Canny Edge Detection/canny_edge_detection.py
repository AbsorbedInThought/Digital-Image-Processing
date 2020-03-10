import cv2 as cv
import numpy as np

#Canny Edge Detector Which Takes An Input Image With Guassian Blur Applied
def myCannyEdgeDetectionAlgo(image):
    
    img = np.asarray(image, dtype= np.float32)
    rows, cols = img.shape
    edgeGradient = np.zeros((rows-1, cols-1), dtype = np.float32)
    angle = np.zeros((rows-1, cols-1), dtype = np.float32)
    
    G_x = np.subtract(img[:rows-1, 1:cols], img[:rows-1, 0:cols-1]) 
    G_y = np.subtract(img[1:rows,:cols-1], img[0:rows-1,:cols-1])

    angle = (np.arctan2(G_y, G_x)*180./np.pi)
    
    G_x = G_x**2
    G_y = G_y**2

    edgeGradient = np.add(G_x, G_y)
    edgeGradient = edgeGradient**0.5   
    
    angle[angle<0] += 180; #180 Degree Phase Shift. To Map Negative Quadrant To Positive Quadrant
    
    suppressionMatrix = np.zeros((rows-1, cols-1), dtype=np.int32)
    
    for i in range(1,rows-2):
        for j in range(1,cols-2):
         #Comparing Neighboring Values For Largest(If it is largest, it is retained)  
         
            #For Direction Above & Below
            if (0 <= angle[i][j] < 22.5) or (157.5 <= angle[i][j] <= 180):
                if(edgeGradient[i][j] > edgeGradient[i][j+1]) and (edgeGradient[i][j] > edgeGradient[i][j-1]):
                    suppressionMatrix[i][j] = edgeGradient[i][j]
                
            #For Direction Diagonally Right To Left
            elif (22.5 <= angle[i][j] < 67.5):
                if(edgeGradient[i][j] > edgeGradient[i+1][j-1]) and (edgeGradient[i][j] > edgeGradient[i-1][j+1]):
                    suppressionMatrix[i][j] = edgeGradient[i][j]
                
            #For Direction Left & Right
            elif (67.5 <= angle[i][j] < 112.5):
                if(edgeGradient[i][j] > edgeGradient[i+1][j]) and (edgeGradient[i][j] > edgeGradient[i-1][j]):
                    suppressionMatrix[i][j] = edgeGradient[i][j]
                    
            #For Direction Diagonally Left To Right
            elif (112.5 <= angle[i][j] < 157.5):
                if(edgeGradient[i][j] > edgeGradient[i-1][j-1]) and (edgeGradient[i][j] > edgeGradient[i+1][j+1]):
                    suppressionMatrix[i][j] = edgeGradient[i][j]
    
    #Double Thresholding
    low = 5
    high = 15
    suppressionMatrix[suppressionMatrix <= low] = 0
    suppressionMatrix[suppressionMatrix >= high] = 255
    
    #Hysterisis
    for i in range(0, rows-2):
        for j in range(0, cols-2):
            if(suppressionMatrix[i][j] != 0 and suppressionMatrix[i][j] != 255):
                if ((suppressionMatrix[i+1, j-1] == 255) or (suppressionMatrix[i+1, j] == 255) or (suppressionMatrix[i+1, j+1] == 255)
                or (suppressionMatrix[i, j-1] == 255) or (suppressionMatrix[i, j+1] == 255)
                or (suppressionMatrix[i-1, j-1] == 255) or (suppressionMatrix[i-1, j] == 255) or (suppressionMatrix[i-1, j+1] == 255)):
                    suppressionMatrix[i, j] = 255
                else:
                    suppressionMatrix[i, j] = 0
        
    return suppressionMatrix
    

readImage = cv.imread("readImage.jpg", 0) #Grayscale
blur = cv.GaussianBlur(readImage,(3,3),0) #Guassian Blur with 3x3 Kernel
output = myCannyEdgeDetectionAlgo(blur)
cv.imwrite("Edge.jpg", output)
            
               
