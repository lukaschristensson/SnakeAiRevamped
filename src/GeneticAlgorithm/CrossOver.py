import numpy as np
import GeneticAlgorithm.Config as Config


def NPointCrossover(net1, net2, n):
    assert net1.topology == net2.topology
    assert net1.unraveledLength() >= n
    resTopology = net1.topology
    crossoverPoint = [int(np.floor(np.random.rand() * net1.unraveledLength()))]
    for i in range(1, n):
        crossoverPoint.append(int(np.floor(np.random.rand() * net1.unraveledLength())))
    crossoverPoint.sort()
    net1 = net1.unraveled()
    net2 = net2.unraveled()

    cursor = 0
    from1 = True
    res1 = np.empty((1, 0))
    res2 = np.empty((1, 0))
    for i in range(len(crossoverPoint)):
        if from1:
            res1 = np.append(res1, net1[cursor:crossoverPoint[i]])
            res2 = np.append(res2, net2[cursor:crossoverPoint[i]])
        else:
            res2 = np.append(res2, net1[cursor:crossoverPoint[i]])
            res1 = np.append(res1, net2[cursor:crossoverPoint[i]])
        from1 = not from1
        cursor = crossoverPoint[i]
    if from1:
        res1 = np.append(res1, net1[cursor:])
        res2 = np.append(res2, net2[cursor:])
    else:
        res2 = np.append(res1, net1[cursor:])
        res1 = np.append(res2, net2[cursor:])

    import NeuralNet.Network as Network
    return Network.fromUnraveled(res1, resTopology), Network.fromUnraveled(res2, resTopology)


def SinglePointCrossover(net1, net2):
    return NPointCrossover(net1, net2, 1)


def TwoPointCrossover(net1, net2):
    return NPointCrossover(net1, net2, 2)


def UniformCrossover(net1, net2):
    assert net1.topology == net2.topology
    resTopology = net1.topology

    res1 = np.zeros(net1.unraveledLength())
    res2 = np.zeros(net1.unraveledLength())

    net1 = net1.unraveled()
    net2 = net2.unraveled()

    for i in range(net1.shape[0]):
        if 0.5 <= np.random.rand():
            res1[i] = net1[i]
            res2[i] = net2[i]
        else:
            res1[i] = net2[i]
            res2[i] = net1[i]
    import NeuralNet.Network as Network
    return Network.fromUnraveled(res1, resTopology), Network.fromUnraveled(res1, resTopology)


def SimulatedBinaryCrossover(net1, net2):
    assert net1.topology == net2.topology
    resTopology = net1.topology
    net1 = net1.unraveled()
    net2 = net2.unraveled()
    rand = np.random.random(net1.shape)
    beta = np.empty(net1.shape)

    beta[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1 / (Config.eta + 1))
    beta[rand > 0.5] = (2 * rand[rand > 0.5]) ** (1 / (Config.eta + 1))

    c1 = 0.5 * ((1 + beta) * net1 + (1 - beta) * net2)
    c2 = 0.5 * ((1 - beta) * net1 + (1 + beta) * net2)
    import NeuralNet.Network as Network
    return Network.fromUnraveled(c1, resTopology), Network.fromUnraveled(c2, resTopology)


CrossOverFunctions = {
    'UniformCrossover': UniformCrossover,
    'SinglePointCrossover': SinglePointCrossover,
    'TwoPointCrossover': TwoPointCrossover,
    'NPointCrossover': NPointCrossover,
    'SimulatedBinaryCrossover': SimulatedBinaryCrossover
}
