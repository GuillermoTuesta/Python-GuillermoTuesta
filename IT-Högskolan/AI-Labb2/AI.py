#import os
#import sys
#print(os.listdir('.'))
#print(sys.argv[0]) 
# good for debugging file handling issues - checks directory and file names.

import matplotlib.pyplot as plt

def Classify(TestPoint, MeasurementList = None, Amount=10): 
	if type(TestPoint) != list:
		print("Classify Function: 'TestPoint' Parameter is not a list!")
		return None
	if TestPoint[0] < 0:
		print("Classify Function: 'X-coordinate is below zero!")
		return None
	if TestPoint[1] < 0:
		print("Classify Function: 'Y-coordinate is negative!")
		return None 
	if Amount <= 0:
		print("Function 'Classify': 'Amount' cannot be zero or negative.")
		return None
	if Amount%2: # I'd love to make this possible.
		print("Function 'Classify': 'Amount' has to be an even number for comparison purposes.")
		return None

	if MeasurementList:
		LocalMeasurementList = [Measurement for Measurement in MeasurementList]
		print("Classify Function: MeasurementList Parameter Error - Defaulting to AllMeasurements list!")
	else:
		LocalMeasurementList = [Measurement for Measurement in AllMeasurements] # NOTE!!! ALL MEASUREMENTS IS DEFAULT AND REFERENCED DIRECTLY. IT CAN BE OVERRIDEN IF MEASUREMENTLIST IS PASSED A LIST.

	#DistanceLambda = lambda GivenList: ((GivenList[0] - TestPoint[0])**2 + (GivenList[1] - TestPoint[1])**2)**(1/2)  # Lambda function to filter the TempList. Used only inside this function.
	#DistanceList = list(map(DistanceLambda, LocalMeasurementList))

	ClassBool = None
	Distances = {}
	ClosestPoints = {}
	while len(ClosestPoints) < Amount:
		SmallestDistance = 9999
		for Measurement in LocalMeasurementList: # Get the smallest value.
			Distance = ((Measurement[0] - TestPoint[0])**2 + (Measurement[1] - TestPoint[1])**2)**(1/2) 
			if Distance < SmallestDistance:
				SmallestDistance = Distance
				ClosestPoint = Measurement

		ClosestPoints[f"Distance{len(ClosestPoints) + 1}"] = ClosestPoint
		Distances[f"Distance{len(ClosestPoints)+ 1}"] = SmallestDistance
		LocalMeasurementList.remove(ClosestPoint)


	PikaPoints = [Point for Point in ClosestPoints.values() if Point[2] == 1] # Create a list of all pikapoints from the closest points.

	if len(PikaPoints) >= Amount/2 + 1: # If the length of the list PikaPoints is equal to or larger than (Amount/2 + 1), then it has won by majority.
		ClassBool = True
	
	if len(PikaPoints) <= Amount/2 - 1: # Similar logic.
		ClassBool = False

	# If there was no majority, move on to a score based on which type the closest points had. The closer the point, the higher the index score given to it's class.
	if ClassBool == None:
		print("Classify Function: Moving onto Index scoring...")
		IndexBonus = Amount
		MajorityPoint = (Amount * ((Amount+1)/2))//2 # Calculates the midway point, making similar comparisons from before possible. Sadly has to be rounded off, though modification to the formula could fix it.
		PikaIndexSum = 0

		for Data in ClosestPoints:
			if Data[2] == 1:
				PikaIndexSum += IndexBonus
			IndexBonus -= 1
	
		if PikaIndexSum >= MajorityPoint + 1:
			ClassBool = True
	
		if PikaIndexSum <= MajorityPoint - 1:
			ClassBool = False
	
	if (ClassBool or not ClassBool) and SaveData:
		Class = 1 if ClassBool else 0
		AdditionalDataPoints.write(f"{[TestPoint[0], TestPoint[1], Class]}\n")
	
	if ClassBool == None:
		print("Testpoint is utterly ambiguous. No majority nor index score winner - This function returns None.")

	return ClassBool # Classbool is None if datapoint couldn't be classified. ClassBool is True if datapoint was classified as Pikachu, and false if it was Pichu.


DataPoints = open("IT-Högskolan/AI-Labb2/datapoints.txt", "r") 
TestPoints = open("IT-Högskolan/AI-Labb2/testpoints.txt", "r") 
AdditionalDataPoints = open("IT-Högskolan/AI-Labb2/AdditionalDatapoints.txt", "a")
# Had weird issues with python not finding the text files despite sharing folders with them. I'll just use the relative path.

DataPoints.readline()
TestPoints.readline() # Skipping the first lines before looping through the files.

PikachuData = []
PichuData = []
for DataPoint in DataPoints:
	DataPoint = DataPoint.split()
	DataArray = [float(DataPoint[0][:-1]), float(DataPoint[1][:-1]), bool(int(DataPoint[2]))]
	if DataPoint[2] == '1':
		PikachuData.append(DataArray)
		continue
	PichuData.append(DataArray)
# Reads file line by line, clean up string and append them as an array.

AllMeasurements = [*PikachuData, *PichuData]

TestMeasurements = []
for TestPoint in TestPoints:
	TestPoint = TestPoint.split()
	TestMeasurements.append([float(TestPoint[1][1:-1]),  float(TestPoint[2][:-1])]) # Some specific string manipulation so I can convert to float.

for LegendIndex, Data in enumerate(PikachuData):
	if not LegendIndex:
		plt.scatter(Data[0], Data[1], label="Pika", color="r") 
		continue
	plt.scatter(Data[0], Data[1], color="r") # Red for Pikachu.

for LegendIndex, Data in enumerate(PichuData):
	if not LegendIndex:
		plt.scatter(Data[0], Data[1], label="Pichu", color="b")
		continue
	plt.scatter(Data[0], Data[1], color="b") # Blue for Pichu.

for LegendIndex, Data in enumerate(TestMeasurements):
	if not LegendIndex:
		plt.scatter(Data[0], Data[1], label="TestPoint", color='black') # Black for test points.
		continue
	plt.scatter(Data[0], Data[1], color="b")

plt.title("Scattered datapoints.")    
plt.xlabel("Width")
plt.ylabel("Height")
plt.legend()
plt.show()

while True:
	UserInput = input(f"Enter two numbers 'a,b' to compare to datapoints (Enter 'exit' to exit program): ")
	if UserInput in 'ExitEXIT':
		print("You have exited the program.")
		break
	UserTestPoint = [float(UserInput.split()[0]), float(UserInput.split()[-1])] # Turn UserInput into list of floats.
	print(f" Classify(UserTestPoint) = {Classify(UserTestPoint)}")