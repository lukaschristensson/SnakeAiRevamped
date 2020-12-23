import numpy as np


def RouletteWheelSelection(Population, numberOfIndividuals):
    NewPopulation = []
    for _ in numberOfIndividuals:
        totalFitness = 0
        for individual in Population:
            totalFitness += individual.getFitness()
        chosenIndividual = np.random.rand() * totalFitness
        totalFitness = Population[0].getFitness()
        cursor = 0
        while totalFitness < chosenIndividual:
            cursor += 1
            totalFitness += [cursor]
        NewPopulation.append(Population[cursor])
        del Population[cursor]
    return NewPopulation


def RankSelection(Population, numberOfIndividuals):
    NewPopulation = []
    for _ in numberOfIndividuals:
        TotalPoints = len(Population) * (len(Population) + 1) / 2




    return NewPopulation
