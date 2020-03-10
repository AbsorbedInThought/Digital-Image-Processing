import cv2

def customConvolve(image, gridSize, offset):
   
    rows, cols = image.shape
    work = image.copy()
    range = int(gridSize/2)
   
    i = gridSize-1
    while(i < rows-gridSize):
        j = gridSize-1
        while(j < cols-gridSize):
            k = i-range
            mean = 0.0
            while(k < i+range):
                l = j - range
                while(l < j+range):
                    mean += image[k][l]
                    l = l+1
                k= k+1    
               
            if(image[i][j] < (mean/(gridSize**2))+offset): 
                work[i][j] = 0
            else:
                work[i][j] = 255
                
            j = j+1
        i = i+1
       
    print("Working")
    return work

my_image = cv2.imread("tools.jpg", 0)
work_image = my_image.copy()

returnImage = customConvolve(image, kernek, major)

#output = my_AdaptiveThreshold(work_image, 11, 2)

cv2.imwrite("color_thresh.jpeg", output)



