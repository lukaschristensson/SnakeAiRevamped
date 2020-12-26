import numpy as np


def RouletteWheelSelection(Population, numberOfIndividuals):
    NewPopulation = []
    for _ in range(numberOfIndividuals):
        totalFitness = 0
        for individual in Population:
            totalFitness += individual.getFitness()
        chosenIndividual = np.random.rand() * totalFitness
        totalFitness = 0
        cursor = 0
        while totalFitness < chosenIndividual:
            totalFitness += Population[cursor].getFitness()
            cursor += 1
        NewPopulation.append(Population[cursor - 1])
        del Population[cursor - 1]
    return NewPopulation


def RankSelection(Population, numberOfIndividuals):
    NewPopulation = []
    for _ in range(numberOfIndividuals):
        totalPoints = len(Population) * (len(Population) + 1) / 2
        chosenIndividual = np.random.rand() * totalPoints
        totalPoints = 0
        cursor = 0
        while totalPoints < chosenIndividual:
            totalPoints += len(Population) - cursor
            cursor += 1
        NewPopulation.append(Population[cursor - 1])
        del Population[cursor - 1]
    return NewPopulation


SelectionFunctions = {
    'RouletteWheelSelection': RouletteWheelSelection,
    'RankSelection': RankSelection
}
