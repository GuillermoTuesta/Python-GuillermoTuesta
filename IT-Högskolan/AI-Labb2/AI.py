#import os
#import sys
#print(os.listdir('.'))
#print(sys.argv[0]) 
# good for debugging file handling issues - checks directory and file names.

import matplotlib.pyplot as plt
import random as rand
import numpy as np

def Classify(TestPoint, MeasurementList, Amount=10):
    ClosestPoints = {}
    while len(ClosestPoints) < Amount:
        SmallestDistance = 999999999999 # Huge number just to get the comparisons going.
        for Measurement in MeasurementList:
            Distance = (Measurement[0]**2 + Measurement[1]**2)**(1/2) 
            if Distance < SmallestDistance:
                SmallestDistance = Measurement
        if SmallestDistance:
            continue
                

                
        
    return None

DataPoints = open("IT-Högskolan/AI-Labb2/datapoints.txt", "r") 
TestPoints = open("IT-Högskolan/AI-Labb2/testpoints.txt", "r") 
# Had weird issues with python not finding the text files despite sharing folders with them.
# I'll just use the relative path.

DataPoints.readline()
TestPoints.readline() # Skipping the first lines before looping through them later on.

PikachuList = []
PichuList = []

for DataPoint in DataPoints:
    DataPoint = DataPoint.split() 
    if DataPoint[-1] == '0':
        PichuList.append(DataPoint)
        continue
    PikachuList.append(DataPoint)
# Turns text line into array of strings. This turns both PikachuList and PichuList into 2D arrays.

PikachuData = [[float(Measurement[0][:-1]),float(Measurement[1][:-1]), int(Measurement[2])] for Measurement in PikachuList]    
PichuData =   [[float(Measurement[0][:-1]),float(Measurement[1][:-1]), int(Measurement[2])] for Measurement in PichuList]     
AllMeasurements = [[float(Measurement[0][:-1]),float(Measurement[1][:-1]), int(Measurement[2])] for Measurement in PikachuList] + [[float(Measurement[0][:-1]),float(Measurement[1][:-1]), int(Measurement[2])] for Measurement in PichuList] 
# Clean up the strings, turn them into float numbers, and put them in their own arrays before inserting them.
# They're now 2D Arrays of the width and height measurements.

TestMeasurements = []
for TestPoint in TestPoints:
    TestPoint = TestPoint.split()
    TestMeasurement = [float(TestPoint[1][1:-1]),  float(TestPoint[2][:-1])] # Some string manipulation so I can convert to float.
    TestMeasurements.append(TestMeasurement)

for Measurement in PikachuData:
    plt.scatter(Measurement[0], Measurement[1], color="r") # Red for Pikachu.

for Measurement in PichuData:
    plt.scatter(Measurement[0], Measurement[1], color="b") # Blue for Pichu.

for Measurement in TestMeasurements:
    plt.scatter(Measurement[0], Measurement[1], color='black') # Black for test points.

plt.title("Scattered....")
plt.annotate('Pikachu datapoint.',
                xy=(PikachuData[0][0], PikachuData[0][1]),
            )           
plt.xlabel("Width")
plt.ylabel("Height")
plt.show()