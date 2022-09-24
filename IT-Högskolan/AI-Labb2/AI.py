#import os
#import sys
#print(os.listdir('.'))
#print(sys.argv[0]) 
# good for debugging file handling issues - checks directory and file names.

import matplotlib.pyplot as plt
import random as rand
import numpy as np

def Classify(TestPoint, MeasurementList, Amount=10):

    if Amount <= 0:
        print("Function 'Classify': Amount cannot be zero or negative.")
        return None

    if Amount%2:
        print("Function 'Classify': Amount has to be an even number for comparison purposes.")
        return None


    ClosestPoints = {}
    Distances = {}
    TempList = [Measurement for Measurement in MeasurementList]
    while len(ClosestPoints) < Amount:
        SmallestDistance = 99999
        for Measurement in TempList:
            Distance = ((Measurement[0] - TestPoint[0])**2 + (Measurement[1] - TestPoint[1])**2)**(1/2) 
            if Distance < SmallestDistance:
                SmallestDistance = Distance
                ClosestPoint = Measurement
        ClosestPoints[f"Distance{len(ClosestPoints) + 1}"] = ClosestPoint
        Distances[f"Distance{len(ClosestPoints)+ 1}"] = SmallestDistance
        TempList.remove(ClosestPoint)


    PikaPoints = [Point for Point in ClosestPoints.values() if Point[2] == 1] # Create a list of all pikapoints from the closest points.

    if len(PikaPoints) >= Amount/2 + 1: # If the length of the list PikaPoints is equal to or larger than (Amount/2 + 1), then it has won by majority.
        return True
    
    if len(PikaPoints) <= Amount/2 - 1: # Similar logic.
        return False
    
    # If there was no majority, move on to a score based on which type the closest points had. The closer the point, the higher the index score given to it's class.
    IndexBonus = Amount
    MajorityPoint = Amount * ((Amount+1)/2)
    PikaIndexSum = 0
    for Data in ClosestPoints:
        if Data[2] == 1:
            PikaIndexSum += IndexBonus
        IndexBonus -= 1
    
    if PikaIndexSum >= MajorityPoint + 1:
        return True
    
    if PikaIndexSum <= MajorityPoint - 1:
        return False
    
    print("Testpoint is utterly ambiguous. No majority nor index score winner - This function returns None.")
    return None # End of the function only reached if I can't classify the given testpoint.


DataPoints = open("IT-Högskolan/AI-Labb2/datapoints.txt", "r") 
TestPoints = open("IT-Högskolan/AI-Labb2/testpoints.txt", "r") 
AdditionalDataPoints = open("IT-Högskolan/AI-Labb2/AdditionalDatapoints.txt", "a")
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

print(Classify(TestMeasurements[1], AllMeasurements))


AdditionalDataFlag = False
if input("Enter either 'Yes' or 'No' to whether you want to use additional collected datapoints or not: ") in 'YesYESyes':
    AdditionalDataFlag = True

AdditionalDataString = ''
if AdditionalDataFlag:
    AdditionalDataString = 'and previously collected '

while True:
    UserTestPoint = input(f"Enter a tuple '(a,b)' to compare to initial {AdditionalDataString}datapoints. ")
    break