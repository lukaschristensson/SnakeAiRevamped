import NeuralNet.Network as Network
import NeuralNet.Config as NNConfig
import GeneticAlgorithm.Config as GAConfig
import SnakeEngine.SnakeRunner as SnakeRunner
import numpy as np


def calculate8Rays(BoardSize, snake, apple):
    directions = {
        'N': [0, -1],
        'NE': [1, -1],
        'E': [1, 0],
        'SE': [1, 1],
        'S': [0, 1],
        'SW': [-1, 1],
        'W': [-1, 0],
        'NW': [-1, -1]
    }
    rayRes = []
    posCursor = [snake[0][0], snake[0][1]]

    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    for d in directions:
        rayHit = False
        while not rayHit:
            posCursor[0] += directions[d][0]
            posCursor[1] += directions[d][1]
            if posCursor[0] < 0 or posCursor[0] >= BoardSize[0] or posCursor[1] < 0 or posCursor[1] >= BoardSize[1]:
                rayHit = True
                rayRes.append(['WALL', 1 - distance(snake[0], posCursor) / (np.sqrt(BoardSize[0]**2 + BoardSize[1]**2))])
            elif posCursor[0] == apple[0] and posCursor[1] == apple[1]:
                rayHit = True
                rayRes.append(['APPLE', 1 - distance(snake[0], posCursor) / (np.sqrt(BoardSize[0]**2 + BoardSize[1]**2))])
            elif posCursor in snake[1:]:
                rayHit = True
                rayRes.append(['TAIL', 1 - distance(snake[0], posCursor) / (np.sqrt(BoardSize[0]**2 + BoardSize[1]**2))])

    return rayRes


def fitnessFunction(steps, apples):
    return steps + (2 ** apples) + (apples ** 2.1) * 500 - (apples ** 1.2) * (0.25 * steps) ** 1.3


class Snake:

    def __init__(self, brain=Network.NeuralNetwork()):
        self.tailDirection = 0  # only used as an input parameter to the brain
        self.brain = brain
        self.lifeSpan = GAConfig.LifeSpan
        self.fitness = -1

    def getFitness(self):
        return self.fitness

    '''
        +8*3 rays, one set of 8 rays for walls, tails and the apple with the distance divided by the longest possible distance (=sqrt(height**2 + width**2))
        +4 one hot inputs for currentDirection
        +4 one hot for the direction of the tail piece that is right behind the head
        = 32 input nodes
    '''

    def nextDir(self, BoardSize, snake, apple, currentDirection, fetchActivations=False):
        appleRays = [0]*8
        wallsRays = [0]*8
        tailsRays = [0]*8

        cursor = 0
        for ray in calculate8Rays(BoardSize, snake, apple):
            if ray[0] == 'WALL':
                wallsRays[cursor] = ray[1]
            elif ray[0] == 'APPLE':
                appleRays[cursor] = ray[1]
            elif ray[0] == 'TAIL':
                tailsRays[cursor] = ray[1]
            cursor += 1
        oneHotDirection = [currentDirection == "North", currentDirection == "East", currentDirection == "South", currentDirection == "West"]
        oneHotTailDirection = [0]*4
        oneHotTailDirection[self.tailDirection] = 1
        inputList = appleRays + wallsRays + tailsRays + oneHotDirection + oneHotTailDirection
        if fetchActivations:
            nnres, activations = self.brain.feedForward(np.asarray(inputList), fetchActivations=fetchActivations)
            self.tailDirection = oneHotDirection[oneHotTailDirection == 1]
            return ['North', 'East', 'South', 'West'][np.argmax(nnres)], activations
        else:
            nnres = self.brain.feedForward(np.asarray(inputList))
            self.tailDirection = oneHotDirection[oneHotTailDirection == 1]
            return ['North', 'East', 'South', 'West'][np.argmax(nnres)]


    def calculateFitness(self):
        if self.fitness == -1:
            rawFitness = SnakeRunner.runForFitness(self)
            self.fitness = fitnessFunction(rawFitness[2], len(rawFitness[0]) - rawFitness[1])
