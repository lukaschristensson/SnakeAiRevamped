import numpy as np


def nPointCrossover(net1, net2, n):
    assert net1.topology == net2.topology
    resTopology = net1.topology
    crossoverPoint = [int(np.floor(np.random.rand() * net1.unraveledLength()))]
    for i in range(1, n):
        crossoverPoint.append(int(np.floor(np.random.rand() * net1.unraveledLength())))
    crossoverPoint.sort()
    net1 = net1.unraveled()
    net2 = net2.unraveled()

    print('expected size: ', net1.shape)

    cursor = 0
    from1 = True
    res1 = np.empty((1, 0))
    res2 = np.empty((1, 0))
    for i in range(len(crossoverPoint)):
        if from1:
            res1 = np.append(res1, net1[cursor:crossoverPoint[i]])
            res2 = np.append(res2, net2[cursor:crossoverPoint[i]])
        else:
            res2 = np.append(res1, net1[cursor:crossoverPoint[i]])
            res1 = np.append(res2, net2[cursor:crossoverPoint[i]])
        from1 = not from1
        cursor += crossoverPoint[i]
    if from1:
        res1 = np.append(res1, net1[cursor:])
        res2 = np.append(res2, net2[cursor:])
    else:
        res2 = np.append(res1, net1[cursor:])
        res1 = np.append(res2, net2[cursor:])

    import NeuralNet.Network as Network
    return Network.fromUnraveled(res1, resTopology), Network.fromUnraveled(res2, resTopology)


def singlePointCrossover(net1, net2):
    return nPointCrossover(net1, net2, 1)


def twoPointCrossover(net1, net2):
    return nPointCrossover(net1, net2, 2)
