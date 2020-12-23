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
    print('starting size: ', unraveled.shape[0])
    for i in range(1, len(topology)):
        newNet.layers.append(
            unraveled[cursor:cursor + (topology[i - 1] + 1) * topology[i]]
            .reshape(topology[i - 1] + 1, topology[i])
        )
        print((topology[i - 1] + 1) * topology[i], ' with ', unraveled.shape[0] - ((topology[i - 1] + 1) * topology[i]) - cursor, 'left')
        cursor += (topology[i - 1] + 1) * topology[i]
    return newNet


class NeuralNetwork:
    def __init__(self, topology, initWeights=True):
        self.topology = topology
        self.layers = []
        if initWeights:
            for i in range(1, len(topology)):
                newLayer = np.random.uniform(-Config.StartingWeight, Config.StartingWeight,
                                             size=(topology[i - 1],
                                                   topology[i]))  # init weights as [-StartingWeight, StartingWeight)
                newLayer = np.r_[newLayer, [np.zeros(topology[i])]]  # biases, init at 0
                self.layers.append(newLayer)
            for layer in self.layers:
                print(layer.shape)
        self.hiddenActivationFunction = ActivationFunctions[Config.HiddenActivationFunction]
        self.outputActivationFunction = ActivationFunctions[Config.OutputActivationFunction]

    def unraveled(self):
        unraveled = self.layers[0].ravel()
        for i in range(1, len(self.layers)):
            unraveled = np.r_[unraveled, self.layers[i].ravel()]
        return unraveled

    def unraveledLength(self):
        return self.unraveled().shape[0]

    def feedForward(self, inputData):
        a = inputData
        for layer in range(0, len(self.layers) - 1):
            a = self.hiddenActivationFunction(np.c_[a, np.ones((1, a.shape[0]))].dot(self.layers[layer]))
        return self.outputActivationFunction(np.c_[a, np.ones((1, a.shape[0]))].dot(self.layers[-1]))
