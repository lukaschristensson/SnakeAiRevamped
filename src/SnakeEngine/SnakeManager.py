import SnakeEngine.Snake as Snake
import NeuralNet.Config as NNConfig
import GeneticAlgorithm.Config as GAConfig
import GeneticAlgorithm.CrossOver as CrossOver
import GeneticAlgorithm.Mutation as Mutation
import GeneticAlgorithm.Selection as Selection
import numpy as np
import multiprocessing
import time
import os
import psutil


def runGeneration(snakePopulation, returnQueue, mutationFunction, crossoverFunction, selectionFunction):
    parents = selectionFunction(snakePopulation, int(len(snakePopulation) / 2))
    for i in range(len(parents)):
        parent1 = parents[int(np.floor(np.random.uniform(0, len(parents))))]
        parent2 = parents[int(np.floor(np.random.uniform(0, len(parents))))]

        childNet1, childNet2 = crossoverFunction(parents[i].brain, parent1.brain)
        childNet3, childNet4 = crossoverFunction(parents[i].brain, parent2.brain)

        snakePopulation.append(Snake.Snake(mutationFunction(childNet1)))
        snakePopulation.append(Snake.Snake(mutationFunction(childNet2)))
        snakePopulation.append(Snake.Snake(mutationFunction(childNet3)))
        snakePopulation.append(Snake.Snake(mutationFunction(childNet4)))

    for s in snakePopulation:
        s.calculateFitness()
    for s in [s for s in snakePopulation if s.lifeSpan < 0]:
        snakePopulation.remove(s)
    returnQueue.put(selectionFunction(snakePopulation, GAConfig.PopulationSize))


class SnakeManager:
    def __init__(self):
        self.populationSize = GAConfig.PopulationSize
        assert self.populationSize % 2 == 0
        self.snakePopulation = []
        for _ in range(self.populationSize):
            addedSnake = Snake.Snake()
            self.snakePopulation.append(addedSnake)
            addedSnake.calculateFitness()
        self.bestSnake = self.snakePopulation[0]
        self.bestFitness = 0

    generation = 0
    maxBitUsage = 0

    def runPopulation(self):
        self.mutationFunction = Mutation.MutationFunctions[GAConfig.MutationFunction]
        self.crossoverFunction = CrossOver.CrossOverFunctions[GAConfig.CrossoverFunction]
        self.selectionFunction = Selection.SelectionFunctions[GAConfig.SelectionFunction]
        while True:
            print('Generation ', SnakeManager.generation, ': ', end='')
            self.startTime = time.time()
            self.returnQueue = multiprocessing.Queue()
            p = multiprocessing.Process(target=runGeneration,
                                        args=(self.snakePopulation, self.returnQueue,
                                              self.mutationFunction,
                                              self.crossoverFunction,
                                              self.selectionFunction
                                              ))
            p.start()
            self.snakePopulation = self.returnQueue.get()
            p.join()
            self.snakePopulation.sort(key=Snake.Snake.getFitness, reverse=True)
            self.bestSnake = self.snakePopulation[0]
            self.bestFitness = self.bestSnake.getFitness()
            for s in self.snakePopulation:
                s.lifeSpan -= 1
            print(str(np.round((time.time() - self.startTime), 4)) + "s", "::", "Best fitness =", self.bestFitness)
            print(np.sum(self.bestSnake.brain.layers[0]))
            SnakeManager.generation += 1
            if False:
                self.currentUsage = psutil.Process(os.getpid()).memory_info().rss
                if SnakeManager.maxBitUsage < self.currentUsage:
                    SnakeManager.maxBitUsage = self.currentUsage
                print("     mem bits used= ", str(np.floor(self.currentUsage / 1000000)) + " mb", "::", "max= ",
                      str(np.floor(SnakeManager.maxBitUsage / 1000000)) + " mb")
