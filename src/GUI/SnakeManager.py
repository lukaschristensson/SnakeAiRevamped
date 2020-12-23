import SnakeEngine.Snake as Snake
import NeuralNet.Config as NNConfig
import GeneticAlgorithm.Config as GAConfig
import GeneticAlgorithm.CrossOver as CrossOver
import GeneticAlgorithm.Mutation as Mutation
import multiprocessing

def runGeneration(snakePopulation):
    #




    pass



class SnakeManager:
    def __init__(self):
        self.populationSize = GAConfig.PopulationSize
        self.snakePopulation = []
        for _ in self.populationSize:
            self.snakePopulation.append(Snake.Snake())
        self.mutationFunction = Mutation.MutationFunctions[GAConfig.MutationFunction]
        self.crossoverFunction = CrossOver.CrossOverFunctions[GAConfig.CrossoverFunciton]
        self.bestSnake = self.snakePopulation[0]

    def runPopulation(self):
        multiprocessing.Process()
