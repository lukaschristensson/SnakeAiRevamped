import numpy as np
import NeuralNet.Config as NNConfig
import GeneticAlgorithm.Config as GAConfig
import GeneticAlgorithm.CrossOver as CrossOver
import GeneticAlgorithm.Mutation as Mutation
import GeneticAlgorithm.Selection as Selection
import multiprocessing
import time
import os
import psutil
import CrappyBird.Bird as Bird
import CrappyBird.BirdRunner as BirdRunner
import NeuralNet.Network as Network


def runGeneration(birdPopulation, returnQueue, mutationFunction, crossoverFunction, selectionFunction):
    parents = selectionFunction(birdPopulation, int(len(birdPopulation) / 2))
    for i in range(len(parents)):
        parent1 = parents[int(np.floor(np.random.uniform(0, len(parents))))]
        parent2 = parents[int(np.floor(np.random.uniform(0, len(parents))))]

        childNet1, childNet2 = crossoverFunction(parents[i].brain, parent1.brain)
        childNet3, childNet4 = crossoverFunction(parents[i].brain, parent2.brain)

        birdPopulation.append(Bird.Bird(mutationFunction(childNet1)))
        birdPopulation.append(Bird.Bird(mutationFunction(childNet2)))
        birdPopulation.append(Bird.Bird(mutationFunction(childNet3)))
        birdPopulation.append(Bird.Bird(mutationFunction(childNet4)))

    for s in birdPopulation:
        s.calculateFitness()
    for s in [s for s in birdPopulation if s.lifeSpan < 0]:
        birdPopulation.remove(s)
    returnQueue.put(selectionFunction(birdPopulation, GAConfig.PopulationSize))


class BirdManager:
    def __init__(self):
        self.populationSize = GAConfig.PopulationSize
        assert self.populationSize % 2 == 0
        self.birdPopulation = []
        for _ in range(self.populationSize):
            self.birdPopulation.append(Bird.Bird(Network.NeuralNetwork(topology=[3, 6, 4, 1])))
        self.bestBird = self.birdPopulation[0]
        self.bestFitness = 0

    generation = 0
    maxBitUsage = 0

    def runPopulation(self):
        self.mutationFunction = Mutation.MutationFunctions[GAConfig.MutationFunction]
        self.crossoverFunction = CrossOver.CrossOverFunctions[GAConfig.CrossoverFunction]
        self.selectionFunction = Selection.SelectionFunctions[GAConfig.SelectionFunction]

        while True:
            print('Generation ', BirdManager.generation, ': ', end='')
            self.startTime = time.time()
            self.returnQueue = multiprocessing.Queue()
            p = multiprocessing.Process(target=runGeneration,
                                        args=(self.birdPopulation, self.returnQueue,
                                              self.mutationFunction,
                                              self.crossoverFunction,
                                              self.selectionFunction
                                              ))
            p.start()
            self.birdPopulation = self.returnQueue.get()
            p.join()
            self.birdPopulation.sort(key=Bird.Bird.getFitness, reverse=True)
            self.bestBird = self.birdPopulation[0]
            self.bestFitness = self.bestBird.getFitness()
            for s in self.birdPopulation:
                s.lifeSpan -= 1
            print(str(np.round((time.time() - self.startTime), 4)) + "s", "::", "Best fitness =", self.bestFitness)
            BirdManager.generation += 1
            if False:
                self.currentUsage = psutil.Process(os.getpid()).memory_info().rss
                if SnakeManager.maxBitUsage < self.currentUsage:
                    SnakeManager.maxBitUsage = self.currentUsage
                print("     mem bits used= ", str(np.floor(self.currentUsage / 1000000)) + " mb", "::", "max= ",
                      str(np.floor(SnakeManager.maxBitUsage / 1000000)) + " mb")