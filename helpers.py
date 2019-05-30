import csv
from skimage import color as clr
import math

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


#TODO: make superclass for Color so that computeDeltaE is less hacky

class ColorHouse:
    def __init__(self, colorInstance, colorsPerHouse):
        self.index = colorInstance.index
        self.assoc = colorInstance.assoc
        self.value = colorInstance.value
        self.myColors = [colorInstance]
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


class Color:
    def __init__(self, index, assoc):
        self.index = index
        self.assoc = assoc
        self.value = colorData[index]
        self.isGrouped = False
        self.houseDist = {}
    def findDistances(self, colorHouses):
        for colorHouse in colorHouses:
            self.houseDist[colorHouse] = computeDeltaE(colorHouse, self)


def diff(first, second):
    """Given two lists, find first - second"""
    second = set(second)
    return [item for item in first if item not in second]


def computeDeltaE(color1, color2):
    color1, color2 = color1.value, color2.value
    return clr.deltaE_ciede2000(color1, color2)


def groupColors(myConcept, houseColors, conceptData, assocRange, colorsPerHouse):
    """For each color house (colors strongly associated with the
    given concept), find COLORSPERHOUSE-1 colors that are weakly
    associated with MYCONCEPT"""

    # create color houses for colors with strong associations to myConcept
    myHouses = [ColorHouse(Color(houseColor[0], houseColor[1]), colorsPerHouse) for houseColor in houseColors]
    numHouses = len(myHouses)

    # Color instances to be put into houses
    colorsToGroup = []

    # use assocRange to find subset of items to be grouped, do not add house colors
    for color in conceptData:
        if color not in houseColors and assocRange[0] <= color[1] and color[1] <= assocRange[1]:
            colorsToGroup.append(Color(color[0], color[1]))
    assert len(colorsToGroup) >= numHouses * (colorsPerHouse - 1), "Not enough colors to group"

    # for each color to be grouped, compute dist to each house
    for color in colorsToGroup:
        color.findDistances(myHouses)

    grouped = 0

    # while all houses are not full: group first color in colorsToGroup
    while False in [house.isFull for house in myHouses]:

        # sort colors by smallest value in dist vector
        colorsToGroup.sort(key=lambda x: min(x.houseDist.values()))

        myColor = colorsToGroup[0]
        assert(not myColor.isGrouped), "Tried to group a grouped color"
        myHouse = None
        for house, assoc in myColor.houseDist.items():
            if assoc == min(myColor.houseDist.values()):
                myHouse = house
        myHouse.addColor(myColor)
        colorsToGroup.pop(0)
        grouped += 1
        print(grouped, myHouse.index)
        for colorToGroup in colorsToGroup:
            if myHouse.isFull:
                colorToGroup.houseDist[myHouse] = math.inf
            else:
                colorToGroup.houseDist[myHouse] += computeDeltaE(colorToGroup, myColor)
                # colorToGroup.houseDist[myHouse] = max(colorToGroup.houseDist[myHouse], computeDeltaE(colorToGroup, myColor))

    return myHouses

