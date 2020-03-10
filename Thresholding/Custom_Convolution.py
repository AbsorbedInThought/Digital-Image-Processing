import cv2 as cv
import numpy as np

#Can be used to apply any kernel such as Sobel, Laplacian etc to an image.

def customConvolve(image, kernel, major):
   
    gridSize, gridSize2 = kernel.shape #Getting Dimensions Of Kernel
    
    rows, cols = image.shape #Getting Dimension Of Image
    work = np.zeros((rows,cols), dtype = int) #Inializinf return image
    range1 = int(gridSize/2) #Calculating Boundaries
    range2 = int(gridSize2/2) 
    
    if(major == 0):
            
        for i in range(gridSize-1, rows-gridSize): #Leaving Boundary Edges
            for j in range(gridSize2-1, cols-gridSize2): #Leaving Boundary Edges
                mean = 0.0
                
                for k in range(i-range1, i+range1): #Applying Kernel
                    for l in range(j-range2, j+range2):
                        mean += (image[k][l] * kernel[k-i][l-j])**2 #Multiplying Pixel With Kernel & Adding 
                    
                work[i][j] += (mean)**0.5 #Taking Square Root
            
    if(major == 1):
        for j in range(gridSize2-1, cols-gridSize2):
            for i in range(gridSize-1, rows-gridSize):  
                mean = 0.0
                
                for k in range(i-range1, i+range1):
                    for l in range(j-range2, j+range2):
                        mean += (image[k][l] * kernel[k-i][l-j])**2 #Multiplying Pixel With Kernel & Adding 
                    
                work[i][j] += (mean)**0.5 #Taking Square Root        
              
    print("Done")
    return work

my_image = cv.imread("readImage.jpg", 0)
work_image = my_image.copy()

kernel = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
major = 1

returnImage = customConvolve(work_image, kernel, major)

cv.imwrite("output.jpg", returnImage)



