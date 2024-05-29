import numpy as np

#Input your desired cargo ratios
desiredRatio = [0.5,0.45,0.05]

#Desired percentage to fill the container
desiredPercentageFilled = .97

#Fill out the cargo dictionary, keeping the same naming conventions and dimensions
cargoDict = {"Cargo 1" : [605, 470, 500],
             "Cargo 2" : [675, 490, 510],
             "Cargo 3" : [1150, 290, 230]}

containerDim = [11800,2340,2690]

cargoNum = len(desiredRatio)

cargoCount = {}

for i in range(1, cargoNum + 1):
    cargoCount["Cargo " + str(i)] = 0

containerVolume = containerDim[0] * containerDim[1] * containerDim[2]

def scaleBoxtoDesiredSize(containerDim, percentToFill):
    originalVol = containerDim[0] * containerDim[1] * containerDim[2]
    targetVol = originalVol * (percentToFill)

    scalingMul = (targetVol / originalVol) ** (1/3)

    xResize = containerDim[0] * scalingMul
    yResize = containerDim[1] * scalingMul
    zResize = containerDim[2] * scalingMul

    return [xResize, yResize, zResize]

containerDim = scaleBoxtoDesiredSize(containerDim, desiredPercentageFilled)

#Finds all splits made in the container according to the specified ratio
#Returns an array with all container splits
def findDivideLength(containerDim, desiredRatio):
    i = 0
    allSplits = [0] * len(desiredRatio)
    print(len(allSplits))
    for item in desiredRatio:
        divideVol = (containerDim[0] * containerDim[1] * containerDim[2]) * item
        divideLength = divideVol/(containerDim[1] * containerDim[2])
        allSplits[i] = divideLength
        i += 1

    return allSplits

allSplit = findDivideLength(containerDim, desiredRatio)

sectionDimensionDict = {}

for i in range (1, cargoNum + 1):
    sectionDimensionDict["Section" + str(i)] = [allSplit[i-1], containerDim[1], containerDim[2]]

print(sectionDimensionDict)
print(cargoDict)

firstSectionDim = [allSplit[0], containerDim[1], containerDim[2]]

secondSectionDim = [allSplit[1], containerDim[1], containerDim[2]]

thirdSectionDim = [allSplit[2], containerDim[1], containerDim[2]]

#Iterates through each cargo and determines which peice of cargo, and which orientation of that cargo 
#minimizes wasted space
def fillExtraSpace(leftOverWidth, sectionDim, sectionNum, leftOverLength):
    minVal = -1
    bestFitCargo = ""
    bestOrientation = 0
    reminaingDimension = 0
    ret = [0,0]
    for cargo in cargoDict:
        widthLeftOver1 = leftOverWidth % cargoDict.get(cargo)[0]
        widthLeftOver2 = leftOverWidth % cargoDict.get(cargo)[1]

        if(widthLeftOver1 == 0 and widthLeftOver2 == 0):
            continue

        if((widthLeftOver1 < minVal and widthLeftOver1 >= 1) or (minVal < 0 and widthLeftOver1 >= 1)):
            bestOrientation = 0
            reminaingDimension = 1
            bestFitCargo = cargo
            minVal = widthLeftOver1

        if(widthLeftOver2 < minVal and widthLeftOver2 >= 1):
            bestOrientation = 1
            reminaingDimension = 0
            bestFitCargo = cargo
            minVal = widthLeftOver2  

    numLeftOverStacked = int(sectionDim[2]/cargoDict.get(bestFitCargo)[2])
    numPutWidthWise = int(leftOverWidth/cargoDict.get(bestFitCargo)[bestOrientation])
    numPutLengthWise = int(sectionDim[0]/cargoDict.get(bestFitCargo)[reminaingDimension])

    if(numLeftOverStacked == 0 or numPutWidthWise == 0 or numPutLengthWise == 0):
        print("No cargo can fit into these dimensions")
        return [0,0]

    if(bestOrientation == 1):
        if(sectionDim[1] % cargoDict.get(bestFitCargo)[bestOrientation] < leftOverLength):
            leftOverLength = sectionDim[1] % cargoDict.get(bestFitCargo)[bestOrientation]
        print("Place", numPutLengthWise, "x", numPutWidthWise, "x", numLeftOverStacked, "of", bestFitCargo, "in section", sectionNum, "with the width side along the container's width side")
    else:
        if(sectionDim[1] % cargoDict.get(bestFitCargo)[bestOrientation] < leftOverLength):
            leftOverLength = sectionDim[1] % cargoDict.get(bestFitCargo)[bestOrientation]
        print("Place", numPutLengthWise, "x", numPutWidthWise, "x", numLeftOverStacked, "of", bestFitCargo, "in section", sectionNum, "with the long side along the container's width side")

    cargoCount[bestFitCargo] += numPutLengthWise * numPutWidthWise * numLeftOverStacked

    ret[0] = numPutLengthWise * numPutWidthWise * numLeftOverStacked * (cargoDict.get(bestFitCargo)[0] * cargoDict.get(bestFitCargo)[1] * cargoDict.get(bestFitCargo)[2])
    ret[1] = leftOverLength

    return ret

#Tests two different container orientations (length-wise and width-wise), and chooses the
#orientation with the least space wasted
def determineOrientations(cargoName, cargoDict, sectionDim, sectionNum):
    leftOverLength = 0
    totVol = 0
    numStacked = int(sectionDim[2]/cargoDict.get(cargoName)[2])

    firstTryLeftoverLen = sectionDim[0] % cargoDict.get(cargoName)[0]
    firstTryLeftoverWidth = sectionDim[1] % cargoDict.get(cargoName)[1]
    firstTryTotalWaste = firstTryLeftoverLen + firstTryLeftoverWidth

    secondTryLeftoverLen = sectionDim[0] % cargoDict.get(cargoName)[1]
    secondTryLeftoverWidth = sectionDim[1] % cargoDict.get(cargoName)[0]
    secondTryTotalWaste = secondTryLeftoverLen + secondTryLeftoverWidth

    if(firstTryTotalWaste <= secondTryTotalWaste):
        placedWidth = int(sectionDim[1]/cargoDict.get(cargoName)[1])
        placedLength = int(sectionDim[0]/cargoDict.get(cargoName)[0])
        print("Section", sectionNum)
        print("Place", placedLength, "x", placedWidth, "x", numStacked, "of", cargoName, "in section", sectionNum, "with the long side along the container's long side")

        cargoCount[cargoName] += placedLength * placedWidth * numStacked

        totVol = placedWidth * placedLength * numStacked * (cargoDict.get(cargoName)[0] * cargoDict.get(cargoName)[1] * cargoDict.get(cargoName)[2])

        extraSpace = fillExtraSpace(firstTryLeftoverWidth, sectionDim, sectionNum, firstTryLeftoverLen)
        print("")
        totVol += extraSpace[0]

        return[extraSpace[1], totVol]
    
    else:
        placedWidth = int(sectionDim[1]/cargoDict.get(cargoName)[0])
        placedLength = int(sectionDim[0]/cargoDict.get(cargoName)[1])
        print("Section", sectionNum)
        print("Place", placedLength, "x", placedWidth, "x", numStacked, "of", cargoName, "in section", sectionNum, "with the width side along the container's long side")

        cargoCount[cargoName] += placedLength * placedWidth * numStacked

        totVol = placedWidth * placedLength * numStacked* (cargoDict.get(cargoName)[0] * cargoDict.get(cargoName)[1] * cargoDict.get(cargoName)[2])

        extraSpace = fillExtraSpace(secondTryLeftoverWidth, sectionDim, sectionNum, secondTryLeftoverLen)

        print("")       
        totVol += extraSpace[0]
        
        return[extraSpace[1], totVol]
    
def getVol(cargoCount, cargoDim):
    return cargoCount * cargoDim[0] * cargoDim[1] * cargoDim[2]

sections = []
totalCargo = []

for i in range(1, cargoNum + 1):
    sections.append(determineOrientations(("Cargo " + str(i)), cargoDict, sectionDimensionDict.get("Section" + str(i)), i))
    totalCargo.append(getVol(cargoCount.get("Cargo " + str(i)), cargoDict.get("Cargo " + str(i))))

lengthLeftOver = 0
totalVolumePacked = 0
for i in range(0, cargoNum):
    lengthLeftOver = lengthLeftOver + sections[i][0]
    totalVolumePacked = totalVolumePacked + sections[i][1]

#-1 referrs to the section of empty volume at the end of the container
print("End Section:")
packEndofContainer = fillExtraSpace(containerDim[1], [lengthLeftOver, containerDim[1], containerDim[2]], -1, lengthLeftOver)
print("")

totalVolumePacked += packEndofContainer[0]


totCargo1 = getVol(cargoCount.get("Cargo 1"), cargoDict.get("Cargo 1"))
totCargo2 = getVol(cargoCount.get("Cargo 2"), cargoDict.get("Cargo 2"))
totCargo3 = getVol(cargoCount.get("Cargo 3"), cargoDict.get("Cargo 3"))

print("Total volume packed:", totalVolumePacked)

print("")

for i in range(1, cargoNum + 1):
    print("Cargo " + str(i) + " Percentage of Total Volume:", 100*(totalCargo[i-1]/totalVolumePacked))

print("")

print("Total percentage of volume filled:", 100*(totalVolumePacked/containerVolume))