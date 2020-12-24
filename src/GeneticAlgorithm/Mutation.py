import numpy as np
import GeneticAlgorithm.Config as Config
import NeuralNet.Config as NNConfig
import NeuralNet.Network as Network

'''
    a few more implementations of mutation functions would be useful, but for now there'll only be one
'''


def StandardMutation(net):
    netTopology = net.topology
    net = net.unraveled()
    for i in range(net.shape[0]):
        if np.random.rand() < Config.MutationRate:
            net[i] += np.random.uniform(-NNConfig.StartingWeight, NNConfig.StartingWeight)
            if net[i] < -NNConfig.StartingWeight:
                net[i] = -NNConfig.StartingWeight
            elif net[i] > NNConfig.StartingWeight:
                net[i] = NNConfig.StartingWeight
    return Network.fromUnraveled(net, netTopology)


MutationFunctions = {
    'StandardMutation': StandardMutation
}
