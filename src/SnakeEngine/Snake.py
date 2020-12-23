import NeuralNet.Network as Network
import NeuralNet.Config as NNConfig
import GeneticAlgorithm.Config as GAConfig


class Snake:

    def __init__(self):
        self.brain = Network.NeuralNetwork()
        self.lifeSpan = GAConfig.LifeSpan
