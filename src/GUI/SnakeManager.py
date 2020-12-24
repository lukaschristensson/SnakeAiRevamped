import SnakeEngine.Snake as Snake
import NeuralNet.Config as NNConfig
import GeneticAlgorithm.Config as GAConfig
import GeneticAlgorithm.CrossOver as CrossOver
import GeneticAlgorithm.Mutation as Mutation
import GeneticAlgorithm.Selection as Selection
import numpy as np
import multiprocessing
import time


def runGeneration(snakePopulation, returnQueue, mutationFunction, crossoverFunction, selectionFunction):
    parents = selectionFunction(snakePopulation, int(len(snakePopulation)/2))
    for i in range(len(parents)):
        parent1 = parents[int(np.floor(np.random.uniform(0, len(parents))))]
        parent2 = parents[int(np.floor(np.random.uniform(0, len(parents))))]
        childNets1 = crossoverFunction(parents[i].brain, parent1.brain)
        childNets2 = crossoverFunction(parents[i].brain, parent2.brain)
        snakePopulation.append(Snake.Snake(mutationFunction(childNets1[0])))
        snakePopulation.append(Snake.Snake(mutationFunction(childNets1[1])))
        snakePopulation.append(Snake.Snake(mutationFunction(childNets2[0])))
        snakePopulation.append(Snake.Snake(mutationFunction(childNets2[1])))
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

    def runPopulation(self):
        mutationFunction = Mutation.MutationFunctions[GAConfig.MutationFunction]
        crossoverFunction = CrossOver.CrossOverFunctions[GAConfig.CrossoverFunction]
        selectionFunction = Selection.SelectionFunctions[GAConfig.SelectionFunction]
        generation = 0
        while True:
            print('Generation ', generation, ': ', end='')
            startTime = time.time()
            returnQueue = multiprocessing.Queue()
            p = multiprocessing.Process(target=runGeneration,
                                        args=(self.snakePopulation, returnQueue,
                                              mutationFunction,
                                              crossoverFunction,
                                              selectionFunction
                                              ))
            p.start()
            self.snakePopulation = returnQueue.get()
            p.join()
            self.snakePopulation.sort(key=Snake.Snake.getFitness, reverse=True)
            self.bestSnake = self.snakePopulation[0]
            self.bestFitness = self.bestSnake.getFitness()
            for s in self.snakePopulation:
                s.lifeSpan -= 1
            print(str(np.round((time.time() - startTime), 4)) + "s", "::", "Best fitness =", self.bestFitness)
            generation += 1
