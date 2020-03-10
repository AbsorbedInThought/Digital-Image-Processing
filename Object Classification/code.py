#Author: Taha

#This code is used to train object classifier on Oxford Dataset.

#Libraries
################################
import glob
import cv2 as cv
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os
import random
import xml.etree.ElementTree as ET
################################

#Defining Macros
################################
#Common Tweaks
DATASET_DISTRIBUTION = 0.9
BLOCK_LENGTH = 50
BLOCK_WIDTH = 50
RESIZE_HEIGHT = 64
RESIZE_WIDTH = 64
NO_OF_IMAGES = 100

#Directory Information
IMAGES_REPO = "Bombay/" #Path to Dataset
XML_ANNOTATIONS = "Bombay_XML/" #Path to Annotation

#HOG Configuration
WINDOW_SIZE = (64,64)
BLOCK_SIZE = (16,16)
BLOCK_STRIDE = (8,8)
CELL_SIZE = (8,8)
NBINS = 9
################################

def computeHOG(image): #Histogram of Oriented Gradients
    hog = cv.HOGDescriptor(WINDOW_SIZE,BLOCK_SIZE,BLOCK_STRIDE,CELL_SIZE,NBINS)
    return hog.compute(image)
    
filename = []
height = np.zeros(NO_OF_IMAGES, dtype = 'uint16')
width = np.zeros(NO_OF_IMAGES, dtype = 'uint16')
xmin = np.zeros(NO_OF_IMAGES, dtype = 'uint16')
ymin = np.zeros(NO_OF_IMAGES, dtype = 'uint16')
xmax = np.zeros(NO_OF_IMAGES, dtype = 'uint16')
ymax = np.zeros(NO_OF_IMAGES, dtype = 'uint16')

def fetch_data():
    
    if not os.path.exists(XML_ANNOTATIONS):
        print("Invalid Directory!")
        return
    
    annotations = glob.glob("{}/*xml".format(XML_ANNOTATIONS))
    
    for i, file in enumerate(annotations):
        reader = ET.parse(file)
        
        filename.append(os.path.join(IMAGES_REPO, reader.findtext("./filename")))
        height[i] = int(reader.findtext("./size/height"))
        width[i] = int(reader.findtext("./size/width")) 
        xmin[i] = int(reader.findtext("./object/bndbox/xmin"))
        ymin[i] = int(reader.findtext("./object/bndbox/ymin"))
        xmax[i] = int(reader.findtext("./object/bndbox/xmax"))
        ymax[i] = int(reader.findtext("./object/bndbox/ymax"))
        
    return


len_training = int(DATASET_DISTRIBUTION*NO_OF_IMAGES)
len_test = int(NO_OF_IMAGES - len_training)
test_set = np.zeros(len_test, dtype = 'uint16')
training_set = np.zeros(len_training, dtype = 'uint16')

def distribute_images(): #Split Test & Training Data Randomly

    index_train = 0
    index_test = 0
    for i in range(0, NO_OF_IMAGES):
        number = random.uniform(0.0, 1.0)
        if(number > 0.1 and index_train < len_training):
            training_set[index_train] = i
            index_train +=1
        elif(index_test < len_test):
            test_set[index_test] = i
            index_test +=1
        else:
            training_set[index_train] = i 
            index_train +=1


def doesOverlap(xmin, ymin, xmax, ymax, x_min, y_min, x_max, y_max):
    if (xmin > x_max or xmax < x_min):
        return False
    if (ymin > y_max or ymax < y_min):
        return False
    return True

def get_chunk(image, xmin, ymin, xmax, ymax):
    
    x_min = 0
    y_min = 0
    x_max = 64
    y_max = 64
    
    rows, cols, channels = image.shape 
    while(doesOverlap(xmin, ymin, xmax, ymax, x_min, y_min, x_max, y_max)):
    

        if(xmax+20 < rows):
            x_min += 20
            x_max += 20
        elif(ymax+20 < cols):
            y_min += 20
            y_max += 20
            x_min = 0
            x_max = 64
        else:
            break;
    
    return image[y_min : y_max, x_min:x_max] 

#**********DRIVER FUNCTION***********#
fetch_data()
distribute_images()


#Computing HOG Vectors Of +ive & -ive Classes
positive_HOG_vectors = []
for i in training_set:
    image = cv.imread(filename[i], 1)
    cropped_image = cv.resize((image[ymin[i]:ymax[i], xmin[i]:xmax[i]]), (RESIZE_HEIGHT,RESIZE_WIDTH))
    positive_HOG_vectors.append(computeHOG(cropped_image))
    
negative_HOG_vectors = []    
for i in test_set:
    image = cv.imread(filename[i], 1)
    img = get_chunk(image, xmin[i], ymin[i], xmax[i], ymax[i]);
    negative_HOG_vectors.append(computeHOG(img))
        
    
#Train any classifier below

#Classifier = RandomForestClassifier(n_estimators = 300, max_depth=None,
#min_samples_split=2, random_state=0, verbose=0, n_jobs=4)    

#training = np.copy(positive_HOG_vectors)
#np.append(training, negative_HOG_vectors)

#Classifier.fit()







        











