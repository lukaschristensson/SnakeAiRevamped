import numpy as np
import NeuralNet.Config as Config

ActivationFunctions = {
    'Identity': lambda x: x,
    'BinaryStep': lambda x: x >= 0,
    'Sigmoid': lambda x: 1 / (1 + np.e ** (-x)),
    'GELU': lambda x: x / (1 + np.e ** (-x)),
    'Tanh': lambda x: np.tanh(x),
    'ReLU': lambda x: x * (0 < x)
}


def fromUnraveled(unraveled, topology):
    newNet = NeuralNetwork(topology, False)
    cursor = 0
    for i in range(1, len(topology)):
        newNet.layers.append(
            unraveled[cursor:cursor + (topology[i - 1] + 1) * topology[i]]
            .reshape(topology[i - 1] + 1, topology[i])
        )
        cursor += (topology[i - 1] + 1) * topology[i]
    return newNet


def ReLU(x):
    return x * (0 < x)


def Sigmoid(x):
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)  # surpress annoying sigmoid func warnings, it results from putting ReLU values into sigmoids(kinda)
    return 1 / (1 + np.e ** (-x))


class NeuralNetwork:
    def __init__(self, topology=Config.Topology, initWeights=True):
        self.topology = topology
        self.layers = []
        if initWeights:
            for i in range(1, len(topology)):
                newLayer = np.random.uniform(-Config.StartingWeight, Config.StartingWeight,
                                             size=(topology[i - 1],
                                                   topology[i]))    # init weights as [-StartingWeight, StartingWeight)

                newLayer = np.r_[newLayer, [np.random.uniform(Config.BiasStartingWeight[0], Config.BiasStartingWeight[1], topology[i])]]  # biases, init at 1
                self.layers.append(newLayer)
        self.hiddenActivationFunction = ReLU  # ActivationFunctions[Config.HiddenActivationFunction] UNDER CONSTRUCTION
        self.outputActivationFunction = Sigmoid     # ActivationFunctions[Config.OutputActivationFunction] UNDER CONSTRUCTION

    def unraveled(self):
        unraveled = self.layers[0].flatten()
        for i in range(1, len(self.layers)):
            unraveled = np.r_[unraveled, self.layers[i].flatten()]
        return unraveled

    def unraveledLength(self):
        return self.unraveled().shape[0]

    def feedForward(self, inputData, fetchActivations=False):
        a = [np.append(inputData, 1), np.append(self.hiddenActivationFunction(np.append(inputData, 1).dot(self.layers[0])), 1)]
        for layer in range(1, len(self.layers) - 1):
            a.append(np.append(self.hiddenActivationFunction(a[-1].dot(self.layers[layer])), 1))
        a.append(self.hiddenActivationFunction(a[-1].dot(self.layers[-1])))
        if fetchActivations:
            return a[-1], a
        else:
            return a[-1]
