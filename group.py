import helpers
import matplotlib.pyplot as plt
import numpy as np
from skimage import color as clr
from scipy.special import comb

def processData(myFolder, assocTol=0.09, numHouses=4, colorsPerHouse=4, assocRange=(0, 0.2), mySeed=42):

    resultsList = []

    # find grouping for each of 12 concepts
    for i in range(12):
        myConcept = i

        # get and sort data from helpers.py
        conceptData = helpers.data[myConcept] # 1xnumColors; correlation for each of numColors colors
        numColors = len(conceptData)
        conceptData =[(i, conceptData[i]) for i in range(numColors)] # [(color index, association)]
        conceptData.sort(key=lambda x: x[1], reverse=True)

        # for plotting
        """colorIndices = [color[0] for color in conceptData]
        colorAssoc = [color[1] for color in conceptData]"""

        # get colors for plotting
        """labBarColors = [helpers.colorData[i] for i in colorIndices] # [[L, a, b]]
        rgbBarColors = [clr.lab2rgb([[labVal]])[0][0] for labVal in labBarColors] # change lab to rgb"""

        # get house colors, i.e. colors strongly associated with myConcept
        houseColors = []
        index = 0
        while len(houseColors) < numHouses:
            houseColors.append(conceptData[index])
            if not (conceptData[index][1] - conceptData[index + 1][1] <= assocTol):
                houseColors = []
            index += 1

        """"# plot
        y_pos = np.arange(numColors)
        plt.bar(y_pos, colorAssoc, color=rgbBarColors)
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.title(helpers.allConcepts[myConcept])
        plt.show()"""

        # group colors
        colorHouses = helpers.groupColors(houseColors, conceptData, assocRange, colorsPerHouse, mySeed)
        resultsList.append(colorHouses)
        print('done')

        # display colors on grid from 2D array
        colorArray = []
        valueArray = []
        for colorHouse in colorHouses:
            colorVec = [colorHouse]
            valueVec = [clr.lab2rgb([[colorHouse.value]])[0][0]]
            for color in colorHouse.myColors:
                colorVec.append(color)
                valueVec.append(clr.lab2rgb([[color.value]])[0][0])
            colorArray.append(colorVec)
            valueArray.append(valueVec)
        plt.imshow(valueArray)
        plt.title(helpers.allConcepts[myConcept])

        # display concept associations over grid
        for i in range(len(colorArray)):
            for j in range((len(colorArray[i]))):
                textColor = 'black'
                if colorArray[i][j].value[0] < 50:
                    textColor = 'white'
                plt.text(j - 0.25, i, str.format('{0:.4f}', colorArray[i][j].assoc), color=textColor)


        plt.savefig(myFolder + '/' + helpers.allConcepts[myConcept] + '.svg', format='svg')
        plt.close()
    print(helpers.calcHeurs(resultsList))


processData('results/changeMe')