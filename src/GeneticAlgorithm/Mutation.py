import numpy as np
import GeneticAlgorithm.Config as Config
import NeuralNet.Config as NNConfig

'''
    a few more implementations of mutation functions would be useful, but for now there'll only be one
'''


def StandardMutation(net):
    net = net.unravled()
    for i in net.shape[0]:
        if np.random.rand() < Config.MutationRate:
            net[i] += np.random.uniform(-NNConfig.StartingWeight, NNConfig.StartingWeight)
            if net[i] < -NNConfig.StartingWeight:
                net[i] = -NNConfig.StartingWeight
            elif net[i] > NNConfig.StartingWeight:
                net[i] = NNConfig.StartingWeight


MutationFunctions = {
    'StandardMutation': StandardMutation
}
