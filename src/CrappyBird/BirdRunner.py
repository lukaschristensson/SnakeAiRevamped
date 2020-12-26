import numpy as np

BirdVisualRadius = 10
PillarFill = 'grey'
BirdFill = 'green'
BackgroundFill = 'sky blue'
GapHeight = 50
SpaceBetweenPillars = 180
BirdOffsetFromLeft = 50
MaxGapDeviation = 100
PillarWidth = 30
JumpStrength = 15
GravityConstant = 1
MaxVerticalSpeed = 9
HorizontalSpeed = 2
BoardSize = [400, 400]


def hasHit(pillar, birdPos):
    if birdPos <= 0 or birdPos >= BoardSize[1]:
        return True

    return pillar[0] + PillarWidth / 2 > BirdOffsetFromLeft > pillar[0] - PillarWidth / 2 and np.abs(pillar[1] - birdPos) > GapHeight


def anyHit(pillars, birdPos):
    hit = False
    for p in pillars:
        hit = hit or hasHit(p, birdPos)
    return hit


def runForFitness(controller):
    birdPos = BoardSize[1] / 2  # init the bird in the middle of the screen
    verticalVelocity = 0    # init verticalVelocity
    score = 0   # straight up the amount of frames (eq to distance traveled) to use as fitness
    pillars = []    # all pillars currently used
    for i in range(np.floor_divide(BoardSize[1], SpaceBetweenPillars) + 1):     # add initial pillars
        newPillar = [(i + 1) * SpaceBetweenPillars, np.random.uniform(-MaxGapDeviation, MaxGapDeviation)]
        pillars.append(newPillar)

    while not anyHit(pillars, birdPos) and score <= 1000000:    # 1m points is considered a perfect bird
        score += 1
        if pillars[0][0] < 0:    # delete all pillars that are off screen and replace them with new ones
            del pillars[0]
            pillars.append([pillars[-1][0] + SpaceBetweenPillars, BoardSize[1] / 2 - np.random.uniform(-MaxGapDeviation, MaxGapDeviation)])
        for p in pillars:
            p[0] -= HorizontalSpeed
        verticalVelocity += GravityConstant - controller.getJump(pillars, birdPos, verticalVelocity) * JumpStrength
        verticalVelocity = np.minimum(verticalVelocity, MaxVerticalSpeed)
        verticalVelocity = np.maximum(verticalVelocity, -MaxVerticalSpeed * 2)
        birdPos += verticalVelocity
    return score


class ControllerReview:
    def __init__(self, controller, canvas, CanvasSize, netCanvas=None):
        self.canvas = canvas
        self.controller = controller
        self.netCanvas = netCanvas

        assert CanvasSize == BoardSize
        self.birdPos = BoardSize[1] / 2  # init the bird in the middle of the screen
        self.verticalVelocity = 0    # init verticalVelocity
        self.score = 0   # straight up the amount of frames (eq to distance traveled) to use as fitness
        self.pillars = []    # all pillars currently used
        for i in range(np.floor_divide(BoardSize[1], SpaceBetweenPillars) + 1):     # add initial pillars
            newPillar = [(i + 1) * SpaceBetweenPillars, BoardSize[1] / 2 - np.random.uniform(-MaxGapDeviation, MaxGapDeviation)]
            self.pillars.append(newPillar)

    def stepAndDraw(self):
        import tkinter as tk
        self.canvas.delete(tk.ALL)
        if self.netCanvas:
            self.netCanvas.delete(tk.ALL)
        self.__drawGame__()
        self.score += 1
        if self.pillars[0][0] < 0:    # delete all pillars that are off screen and replace them with new ones
            del self.pillars[0]
            self.pillars.append([self.pillars[-1][0] + SpaceBetweenPillars, BoardSize[1] / 2 - np.random.uniform(-MaxGapDeviation, MaxGapDeviation)])
        for p in self.pillars:
            p[0] -= HorizontalSpeed
        if self.netCanvas:
            shouldJump, activations = self.controller.getJump(self.pillars, self.birdPos, self.verticalVelocity, fetchActivations=True)
        else:
            shouldJump = self.controller.getJump(self.pillars, self.birdPos, self.verticalVelocity)
        self.verticalVelocity += GravityConstant - shouldJump * JumpStrength
        self.verticalVelocity = np.minimum(self.verticalVelocity, MaxVerticalSpeed)
        self.verticalVelocity = np.maximum(self.verticalVelocity, -MaxVerticalSpeed * 2)
        self.birdPos += self.verticalVelocity
        if self.netCanvas:
            self.drawNet(activations, self.netCanvas, self.controller.brain.layers.copy())

        return not anyHit(self.pillars, self.birdPos)

    def reset(self, controller=None):
        if controller:
            self.controller = controller
        self.birdPos = BoardSize[1] / 2  # init the bird in the middle of the screen
        self.verticalVelocity = 0    # init verticalVelocity
        self.score = 0   # straight up the amount of frames (eq to distance traveled) to use as fitness
        self.pillars = []    # all pillars currently used
        for i in range(np.floor_divide(BoardSize[1], SpaceBetweenPillars) + 1):     # add initial pillars
            self.pillars.append([(i + 1) * SpaceBetweenPillars, BoardSize[1] / 2 - np.random.uniform(-MaxGapDeviation, MaxGapDeviation)])


    def __drawGame__(self):
        from tkinter import ALL
        self.canvas.delete(ALL)

        self.canvas.create_rectangle(0, 0, BoardSize[0], BoardSize[1], fill=BackgroundFill)

        for p in self.pillars:
            self.__drawPillar__(p)
        self.__drawBird__(self.birdPos)

    def __drawPillar__(self, pillar):
        # top pillar
        self.canvas.create_rectangle(pillar[0] - PillarWidth/2, 0, pillar[0] + PillarWidth/2, pillar[1] - GapHeight, fill=PillarFill)
        # bottom pillar
        self.canvas.create_rectangle(pillar[0] - PillarWidth/2, pillar[1] + GapHeight, pillar[0] + PillarWidth/2, BoardSize[1], fill=PillarFill)

    def __drawBird__(self, birdPos):
        self.canvas.create_oval(BirdOffsetFromLeft - BirdVisualRadius, birdPos - BirdVisualRadius, BirdOffsetFromLeft + BirdVisualRadius, birdPos + BirdVisualRadius, fill=BirdFill)

    '''
        this shit is ripped straight out of the first project, it kinda looked cool and i can't be arsed to redo it
    '''

    @staticmethod
    def drawNet(activations, netCanvas, net):

        def drawCircle(p, fill, size, canvas):
            canvas.create_oval(p[0], p[1],
                               p[0] + size, p[1] + size,
                               fill=fill)

        def ColorFromrgb(rgb):
            rgb = (rgb[0] * (rgb[0] >= 0), rgb[1] * (rgb[1] >= 0), rgb[2] * (rgb[2] >= 0))
            return "#%02x%02x%02x" % rgb

        # make the background gray
        netCanvas.create_rectangle(0, 0, netCanvas.winfo_width(), netCanvas.winfo_height(), fill='#aaa',
                                   outline="")

        # amount of layers in the net
        layerCount = len(activations)

        # calculate largest column for the orb size
        largestColumn = 0
        for i in range(len(activations)):
            if len(activations[i]) > largestColumn:
                largestColumn = len(activations[i])

        # all layers have the same x offset, calculated here
        xPadding = 50
        layerXPos = netCanvas.winfo_width() / (layerCount + 1)

        # largest y offset found to create the largest orb size possible while still fitting in all the orbs in every layer
        maxOrbSize = 40
        largestLayerYPos = netCanvas.winfo_height() / (largestColumn + 1)
        orbsSize = min(layerXPos, largestLayerYPos) / 1.1
        orbsSize = np.minimum(orbsSize, maxOrbSize)

        layerYPos = []
        # get the y offset for each orb in layer i to space them evenly
        for i in range(layerCount):
            layerYPos.append(netCanvas.winfo_height() / (len(activations[i]) + 1))

        getOrbPos = lambda layer, weightIndex: \
            (xPadding + (layer + 1) * layerXPos - (orbsSize / 2),
             netCanvas.winfo_height() - ((weightIndex + 1) * layerYPos[layer]))

        # draw weights
        for tIndex in range(len(net)):
            t = net[tIndex].copy()
            maxWeight = np.max(np.abs(t))
            for i in range(t.shape[0]):
                rangeList = []
                for k in range(t.shape[1]):
                    rangeList.append(k)
                np.random.shuffle(rangeList)
                for j in rangeList:
                    posOfFromOrb = getOrbPos(tIndex, i)
                    posOfToOrb = getOrbPos(tIndex + 1, j)
                    weightColor = int(np.round(255 * (t[i, j] / maxWeight)))

                    if weightColor < 0:
                        netCanvas.create_line(posOfFromOrb[0], posOfFromOrb[1], posOfToOrb[0], posOfToOrb[1],
                                              width=1,
                                              fill=ColorFromrgb(
                                                  (255, 255 + weightColor, 255 + weightColor)))
                    else:
                        netCanvas.create_line(posOfFromOrb[0], posOfFromOrb[1], posOfToOrb[0], posOfToOrb[1],
                                              width=1,
                                              fill=ColorFromrgb(
                                                  (255 - weightColor, 255, 255 - weightColor)))
        # draw activation orbs
        for i in range(layerCount):
            for j in range(len(activations[i])):
                fill = ''
                # activationStrength is calculated as a percentage of the largest activation
                nodeActivationStrength = int(np.round(
                    255 * ((activations[i][j] / np.max(activations[i])) if np.max(activations[i]) != 0 else 0)))
                if len(activations[i]) == 1:
                    nodeActivationStrength = 255*(activations[i][0] > 0.5)
                if j == len(activations[i]) - 1 and i != layerCount - 1:
                    fill = ColorFromrgb((0, 0, nodeActivationStrength))
                else:
                    fill = ColorFromrgb((nodeActivationStrength, 0, nodeActivationStrength))

                orbPos = getOrbPos(i, j)
                drawCircle(
                    (orbPos[0] - orbsSize / 2, orbPos[1] - orbsSize / 2),
                    fill,
                    orbsSize, netCanvas)
