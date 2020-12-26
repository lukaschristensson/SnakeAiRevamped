import numpy as np
import NeuralNet.Network as Network
import GeneticAlgorithm.Config as GAConfig
import CrappyBird.BirdRunner as BirdRunner


class Bird:
    def __init__(self, brain=Network.NeuralNetwork()):
        self.brain = brain
        self.lifeSpan = GAConfig.LifeSpan
        self.fitness = -1

    def getFitness(self):
        return self.fitness

    def getJump(self, pillars, birdPos, verticalVelocity, fetchActivations=False):
        distToPillarGap = [pillars[0][0] - BirdRunner.BirdOffsetFromLeft, birdPos - pillars[0][1]]
        res = self.brain.feedForward(np.asarray(distToPillarGap + [verticalVelocity]), fetchActivations)
        if fetchActivations:
            return np.round(res[0][0]) == 1, res[1]
        else:
            return np.round(res[0]) == 1

    def calculateFitness(self):
        if self.fitness == -1:
            self.fitness = BirdRunner.runForFitness(self)
            return self.fitness
