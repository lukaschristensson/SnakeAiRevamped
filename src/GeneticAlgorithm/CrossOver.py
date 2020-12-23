import numpy as np


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

    import src.NeuralNet.Network as Network
    return Network.fromUnraveled(res1, resTopology), Network.fromUnraveled(res2, resTopology)


def SinglePointCrossover(net1, net2):
    return NPointCrossover(net1, net2, 1)


def TwoPointCrossover(net1, net2):
    return NPointCrossover(net1, net2, 2)


def UniformCrossover(net1, net2):
    assert net1.topology == net2.topology
    resTopology = net1.topology
    res1 = [0]*net1.unraveledLength()
    res2 = [0]*net1.unraveledLength()
    for i in range(net1.unraveledLength()):
        if 0.5 <= np.random.rand():
            res1[i] = net1[i]
            res2[i] = net2[i]
        else:
            res1[i] = net2[i]
            res2[i] = net1[i]
    import src.NeuralNet.Network as Network
    return Network.fromUnraveled(res1, resTopology), Network.fromUnraveled(res1, resTopology)
