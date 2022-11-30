#import os
#import sys
#print(os.listdir('.'))
#print(sys.argv[0]) 
# good for debugging file handling issues - checks directory and file names.

import matplotlib.pyplot as plt
import sys 
import os # sys and os imported to make file pathing easier.

def Classify(TestPoint, SaveData = False, AdditionalData = False, Amount=10): 
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

	LocalMeasurementList = AllMeasurements
	if AdditionalData:
		print("test")

	ClassBool = None
	Distances = {}
	ClosestPoints = {}
	while len(ClosestPoints) < Amount:
		SmallestDistance = 9999
		for Measurement in LocalMeasurementList: # Get the smallest value.
			Distance = (Measurement[0] - TestPoint[0])**2 + (Measurement[1] - TestPoint[1])**2)**(1/2) 
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
	
	if (ClassBool == True or ClassBool == False) and SaveData:
		AdditionalDataAppend.write(f"{[TestPoint[0], TestPoint[1], ClassBool]}\n") # Append to additional datapoints file if SaveData is true and the point was classified.
	
	if ClassBool == None:
		print("Testpoint is utterly ambiguous. No majority nor index score winner - This function returns None. Appended to AmbiguousPoints.txt.")
		AmbiguousPoints.write(f"{[TestPoint[0], TestPoint[1], ClassBool]}\n")

	return ClassBool # Classbool is None if datapoint couldn't be classified. ClassBool is True if datapoint was classified as Pikachu, and false if it was Pichu.


DataPoints = open(os.path.join(sys.path[0] , "datapoints.txt"), "r")  
TestPoints = open(os.path.join(sys.path[0] , "testpoints.txt"), "r") 
AdditionalDataAppend = open(os.path.join(sys.path[0] , "AdditionalDatapoints.txt"), "a")
AdditionalDataRead =  open(os.path.join(sys.path[0] , "AdditionalDatapoints.txt"), "r")
AmbiguousPoints = open(os.path.join(sys.path[0] , "AmbiguousPoints.txt"), "a") 
#This is why I imported sys and os. 

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

AllMeasurements = [*PikachuData, *PichuData] # To more easily loop through all relevant data.

TestMeasurements = []
for TestPoint in TestPoints:
	TestPoint = TestPoint.split()
	TestMeasurements.append([float(TestPoint[1][1:-1]),  float(TestPoint[2][:-1])]) # Some specific string manipulation so I can convert to float.

AdditionalData = []
for AdditionalDataPoint in AdditionalDataRead:
	SplitPoint = AdditionalDataPoint.split(',')
	ClassNum = 1 if SplitPoint[-1] == "True" else 0
	AdditionalData.append([float(SplitPoint[0][1:]), float(SplitPoint[1]), bool(ClassNum)])

for LegendIndex, Data in enumerate(PikachuData):
	if not LegendIndex:
		plt.scatter(Data[0], Data[1], label="Pikachu data points", color="r") # LegendIndex is used to apply the label only once.
		continue
	plt.scatter(Data[0], Data[1], color="r") # Red for Pikachu.

for LegendIndex, Data in enumerate(PichuData):
	if not LegendIndex:
		plt.scatter(Data[0], Data[1], label="Pichu data points", color="b")
		continue
	plt.scatter(Data[0], Data[1], color="b") # Blue for Pichu.

for LegendIndex, Data in enumerate(TestMeasurements):
	if not LegendIndex:
		plt.scatter(Data[0], Data[1], label="Test data Points", color='black') # Black for test points.
		continue
	plt.scatter(Data[0], Data[1], color="b")

UserAdditionalFlag = input("Input Y/N to whether you want to use additional datapoints (AdditionalDatapoints.txt) along with Datapoints.txt: ")
AdditionalDataFlag = False

if UserAdditionalFlag.lower() in "yes":
	print("Adding and plotting additional (Pink) datapoints...\n")
	AdditionalDataFlag = True
	AllMeasurements += AdditionalData # Adds the additional data to all measurements to be used.
	for LegendIndex, Data in enumerate(AdditionalData):
		if not LegendIndex:
			plt.scatter(Data[0], Data[1], label="Additional Datapoints", color='Pink') # Pink for Additional Data points.
			continue
		plt.scatter(Data[0], Data[1], color="Pink")

plt.title("Scattered datapoints.")    
plt.xlabel("Width(cm)")
plt.ylabel("Height(cm)")
plt.legend()
plt.show()	#Could also consider putting this inside the loop somehow to show the plot after each entered datapoint if wanted by the user.

while True:
	UserInput = input(f"Enter two numbers 'a,b' to compare to datapoints (Enter a variation of 'exit' or nothing to exit): ")
	if UserInput.lower() in 'exit' or UserInput == ' ':
		break
	print("Classifying.. \n")
	UserTestPoint = [float(UserInput.split(',')[0]), float(UserInput.split(',')[-1])] # Turn UserInput into list of floats.
	print(f" Classify(UserTestPoint) = {Classify(UserTestPoint, SaveData = True)}")

print("Exiting program..")