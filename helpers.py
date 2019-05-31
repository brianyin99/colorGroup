import csv
from skimage import color as clr
import math
from abc import ABC
import numpy as np
import random

# Concept names; indices align with data_clean.csv
allConcepts = ['mango','watermelon','honeydew','cantaloupe','grapefruit','strawberry','raspberry','blueberry',
               'avocado','orange','lime','lemon']


# Get the color ratings data from file data_clean.csv ([12x58], i.e. [concepts x colors])
# https://stackoverflow.com/questions/37173892/convert-from-csv-to-array-in-python
data = []
with open("data_clean.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        data.append(row)


# Get the LAB coordinates of colors from file Lab.csv ([58x3], i.e. [colors x LAB coordinates])
colorData = []
with open("Lab.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        colorData.append(row)

class ColorAbstract(ABC):
    """Abstract color class that stores index, association to a given concept, and CIELAB value"""
    def __init__(self, index, assoc):
        self.index = index
        self.assoc = assoc

    @property
    def value(self):
        return colorData[self.index]


class ColorReal(ColorAbstract):
    def __init__(self, index, assoc):
        super().__init__(index, assoc)
        self.isGrouped = False
        self.houseWeights = {}

    """def findWeights(self, colorHouses):
        for colorHouse in colorHouses:
            self.houseWeights[colorHouse] = clr.deltaE_ciede2000(colorHouse.value, self.value)"""

    def updateWeights(self, colorHouses):

        # update weight for each house
        for colorHouse in colorHouses:

            allDeltaEs = []
            valueList = [self.value]

            for myColor in colorHouse.myColors:
                valueList.append(myColor.value)

            # add all pairwise delta Es to allDeltaEs
            for i in range(len(valueList)):
                for j in range(i + 1, len(valueList)):
                    allDeltaEs.append(clr.deltaE_ciede2000(valueList[i], valueList[j]))

            houseWeight = np.var(allDeltaEs)
            # houseWeight = max(allDeltaEs) - min(allDeltaEs)
            # houseWeight = 13

            if not (colorHouse in self.houseWeights and self.houseWeights[colorHouse] == math.inf):
                self.houseWeights[colorHouse] = houseWeight


class ColorHouse(ColorAbstract): # self is not in myColors
    def __init__(self, index, assoc, colorsPerHouse):
        super().__init__(index, assoc)
        self.myColors = []
        self.capacity = colorsPerHouse

    @property
    def numColors(self):
        return len(self.myColors)

    @property
    def isFull(self):
        return self.numColors == self.capacity

    def addColor(self, myColor):
        self.myColors.append(myColor)
        myColor.isGrouped = True


def diff(first, second):
    """Given two lists, find first - second"""
    second = set(second)
    return [item for item in first if item not in second]

def calcHeurs(allResults): #allResults is [myHouses, myHouses, myHouses]
    allVars = []
    allDiffs = []
    for myHouses in allResults:
        for myHouse in myHouses:
            allDeltaEs = []
            valueList = [myHouse.value]

            for myColor in myHouse.myColors:
                valueList.append(myColor.value)

            # add all pairwise delta Es to allDeltaEs
            for i in range(len(valueList)):
                for j in range(i + 1, len(valueList)):
                    allDeltaEs.append(clr.deltaE_ciede2000(valueList[i], valueList[j]))
            allVars.append(np.var(allDeltaEs))
            allDiffs.append(max(allDeltaEs) - min(allDeltaEs))

    return (sum(allVars)/len(allVars), sum(allDiffs)/len(allDiffs))


def groupColors(myConcept, houseColors, conceptData, assocRange, colorsPerHouse, mySeed):
    """For each color house (colors strongly associated with the
    given concept), find COLORSPERHOUSE colors that are weakly
    associated with MYCONCEPT"""

    # create color houses for colors with strong associations to myConcept
    myHouses = [ColorHouse(houseColor[0], houseColor[1], colorsPerHouse) for houseColor in houseColors]
    numHouses = len(myHouses)

    # Color instances to be put into houses
    colorsToGroup = []

    # use assocRange to find subset of items to be grouped, do not add house colors
    for color in conceptData:
        if color not in houseColors and assocRange[0] <= color[1] and color[1] <= assocRange[1]:
            colorsToGroup.append(ColorReal(color[0], color[1]))

    # remove white?
    # colorsToGroup = [colorReal for colorReal in colorsToGroup if colorReal.value != [100, 0, 0]]

    assert len(colorsToGroup) >= numHouses * (colorsPerHouse), "Not enough colors to group, try increasing assocRange"

    """"# for each color to be grouped, compute weight of each house
    for color in colorsToGroup:
        color.findWeights(myHouses)"""

    # pseudorandomly group first numHouses colors
    random.seed(mySeed)
    for i in range(numHouses):
        choice = random.choice(colorsToGroup)
        myHouses[i].addColor(choice)
        colorsToGroup.remove(choice)

    # update house weights for each colorToGroup
    for colorToGroup in colorsToGroup:
        colorToGroup.updateWeights(myHouses)


    grouped = 4

    # while all houses are not full: group first color in colorsToGroup
    while False in [house.isFull for house in myHouses]:

        # sort colors by smallest value in weight vector
        colorsToGroup.sort(key=lambda x: min(x.houseWeights.values()))

        myColor = colorsToGroup[0]
        assert(not myColor.isGrouped), "Tried to group a grouped color"
        myHouse = None
        for house, assoc in myColor.houseWeights.items():
            if assoc == min(myColor.houseWeights.values()):
                myHouse = house
        myHouse.addColor(myColor)
        colorsToGroup.pop(0)
        grouped += 1
        print(grouped, myHouse.index)
        """for colorToGroup in colorsToGroup:
            if myHouse.isFull:
                colorToGroup.houseWeights[myHouse] = math.inf
            else:
                colorToGroup.houseWeights[myHouse] += clr.deltaE_ciede2000(colorToGroup.value, myColor.value)
                # colorToGroup.houseWeights[myHouse] = max(colorToGroup.houseWeights[myHouse], clr.deltaE_ciede2000(colorToGroup.value, myColor.value))"""

        for colorToGroup in colorsToGroup:
            if myHouse.isFull:
                colorToGroup.houseWeights[myHouse] = math.inf
            colorToGroup.updateWeights(myHouses)

    return myHouses

