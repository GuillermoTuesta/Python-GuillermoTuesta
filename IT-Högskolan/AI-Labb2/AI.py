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
TestPoints = open("c:/OD/OneDrive - onmidroc/Documents/Github/Python-GuillermoTuesta/IT-Högskolan/AI-Labb2/testpoints.txt", "r")

DataPoints.readline() # Skipping the first line.

PikachuList = []
PichuList = []

for DataPoint in DataPoints:
    DataPoint = DataPoint.split() # Turns text line into an array. This turns both PikachuList and PichuList into 2D arrays.
    if DataPoint[-1] == '0':
        PichuList.append(DataPoint)
        continue
    PikachuList.append(DataPoint)

PikachuMeasurements = [[Measurement[0],Measurement[1]] for Measurement in PikachuList]
PichuMeasurements = [[Measurement[0],Measurement[1]] for Measurement in PichuList]

for Measurement in PikachuMeasurements:
    plt.scatter(Measurement[0], Measurement[1], color="r")

for Measurement in PichuMeasurements:
    plt.scatter(Measurement[0], Measurement[1], color="b")

plt.show()