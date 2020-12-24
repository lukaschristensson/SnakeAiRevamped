import numpy as np


def RouletteWheelSelection(Population, numberOfIndividuals):
    NewPopulation = []
    for _ in range(numberOfIndividuals):
        totalFitness = 0
        for individual in Population:
            totalFitness += individual.getFitness()
        chosenIndividual = np.random.rand() * totalFitness
        totalFitness = Population[0].getFitness()
        cursor = 0
        while totalFitness < chosenIndividual:
            cursor += 1
            totalFitness += Population[cursor].getFitness()
        NewPopulation.append(Population[cursor])
        del Population[cursor]
    return NewPopulation


def RankSelection(Population, numberOfIndividuals):
    NewPopulation = []
    for _ in numberOfIndividuals:
        totalPoints = len(Population) * (len(Population) + 1) / 2
        chosenIndividual = np.random.rand() * totalPoints
        totalPoints = len(Population)
        cursor = 0
        while totalPoints < chosenIndividual:
            cursor += 1
            totalPoints += len(Population) - cursor
        NewPopulation.append(Population[cursor])
        del NewPopulation[cursor]
    return NewPopulation


SelectionFunctions = {
    'RouletteWheelSelection': RouletteWheelSelection,
    'RankSelection': RankSelection
}
