#import os
#import sys
#print(os.listdir('.'))
#print(sys.argv[0]) 
# good for debugging file handling issues - checks directory and file names.

import matplotlib.pyplot as plt
import random as rand
import numpy as np

TestFile = open("TestFile.txt", "r")
DataPoints = open("c:/OD/OneDrive - onmidroc/Documents/Github/Python-GuillermoTuesta/IT-Högskolan/AI-Labb2/datapoints.txt", "r") 
TestPoints = open("c:/OD/OneDrive - onmidroc/Documents/Github/Python-GuillermoTuesta/IT-Högskolan/AI-Labb2/testpoints.txt", "r") # Had weird issues with python not finding the text files despite sharing folders with them.

DataPoints.readline()
TestPoints.readline() # Skipping the first lines before looping through them later on.

PikachuList = []
PichuList = []

for DataPoint in DataPoints:
    DataPoint = DataPoint.split() # Turns text line into array of strings. This turns both PikachuList and PichuList into 2D arrays.
    if DataPoint[-1] == '0':
        PichuList.append(DataPoint)
        continue
    PikachuList.append(DataPoint)



PikachuMeasurements = [[float(Measurement[0][:-1]),float(Measurement[1][:-1])] for Measurement in PikachuList]    # Clean up the strings, turn them into float numbers, and put them in their own arrays before inserting them.
PichuMeasurements =   [[float(Measurement[0][:-1]),float(Measurement[1][:-1])] for Measurement in PichuList]      # So just 2D Arrays of the width and height measurements.

TestMeasurements = []
for TestPoint in TestPoints:
    TestPoint = TestPoint.split()
    TestMeasurement = [float(TestPoint[1][1:-1]),  float(TestPoint[2][:-1])]
    TestMeasurements.append(TestMeasurement)

for Measurement in PikachuMeasurements:
    plt.scatter(Measurement[0], Measurement[1], color="r") # Pikachu data points will be colored red.

for Measurement in PichuMeasurements:
    plt.scatter(Measurement[0], Measurement[1], color="b") # Blue for Pichu.

for Measurement in TestMeasurements:
    plt.scatter(Measurement[0], Measurement[1], color='black') # Black for test points.

plt.show()


