import helpers
import matplotlib.pyplot as plt
import numpy as np
from skimage import color as clr
from scipy.special import comb

def processData(myFolder, assocTol=0.07, numHouses=4, colorsPerHouse=4, assocRange=(0, 0.2)):

    # all delta E values for all groups across all fruits
    allDeltaEsGlobal = []

    # find grouping for each of 12 concepts
    for i in range(12):
        myConcept = i

        # get and sort data from helpers.py
        conceptData = helpers.data[myConcept] # 1xnumColors; correlation for each of numColors colors
        numColors = len(conceptData)
        conceptData =[(i, conceptData[i]) for i in range(numColors)] # [(color index, association)]
        conceptData.sort(key=lambda x: x[1], reverse=True)
        colorIndices = [color[0] for color in conceptData]
        colorAssoc = [color[1] for color in conceptData]

        """# get colors for plotting
        labBarColors = [helpers.colorData[i] for i in colorIndices] # [[L, a, b]]
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
        colorHouses = helpers.groupColors(myConcept, houseColors, conceptData, assocRange, colorsPerHouse)
        print('done')

        # display colors
        dispArray = []
        for colorHouse in colorHouses:
            groupVec = [clr.lab2rgb([[colorHouse.value]])[0][0]]
            for color in colorHouse.myColors:
                groupVec.append(clr.lab2rgb([[color.value]])[0][0])
            dispArray.append(groupVec)

        deltaEtriplesConcept = []

        # calculate (sum(delta E), mean(delta E), max(delta E)) per row
        for colorHouse in colorHouses:
            allDeltaEs = []
            colorVec = [colorHouse.value]
            for color in colorHouse.myColors:
                colorVec.append(color.value)
            for i in range(len(colorVec)):
                for j in range(i + 1, len(colorVec)):
                    allDeltaEs.append(clr.deltaE_ciede2000(colorVec[i], colorVec[j]))
                    allDeltaEsGlobal.append(clr.deltaE_ciede2000(colorVec[i], colorVec[j]))

            assert len(allDeltaEs) == comb((colorsPerHouse + 1), 2), "combinations done incorrectly"
            deltaEtripleHouse = (sum(allDeltaEs), sum(allDeltaEs)/len(allDeltaEs), max(allDeltaEs))
            deltaEtriplesConcept.append(deltaEtripleHouse)


        plt.imshow(dispArray)
        plt.title(helpers.allConcepts[myConcept])
        plt.savefig(myFolder + '/' + helpers.allConcepts[myConcept] + '.svg', format='svg')

    deltaEtripleGlobal = (sum(allDeltaEsGlobal), sum(allDeltaEsGlobal)/len(allDeltaEsGlobal), max(allDeltaEsGlobal))
    print(deltaEtripleGlobal)


processData('results/0.07 sum no white triple')