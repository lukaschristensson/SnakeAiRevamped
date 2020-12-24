import numpy as np

# config
BoardSize = [20, 20]
SnakeInitSize = 4
StepsUntilStarve = 150
# util/enum
Directions = {
    "North": [0, -1],
    "East": [1, 0],
    "South": [0, 1],
    "West": [-1, 0]
}
'''
    :argument snake is a list of tails, including the head
    :returns a position within the bounds of @BoardSize
'''


def generateApplePos(snake=None):
    if not snake:
        return None
    possibleTiles = []
    for i in range(BoardSize[0]):
        for j in range(BoardSize[1]):
            if not snake.__contains__([i, j]):
                possibleTiles.append([i, j])
    return None if len(possibleTiles) == 0 else possibleTiles[int(np.floor(np.random.random() * len(possibleTiles)))]


'''
    :argument snake is a list of tails, including the head
    :argument currentDirection is a string which matches an entry in the Direction dictionary
'''


def advanceSnake(snake=None, currentDirection=None):
    if not snake:
        return None
    for i in reversed(range(1, len(snake))):  # advance all tail pieces
        snake[i] = snake[i - 1]
    snake[0] = [snake[0][0] + Directions[currentDirection][0],
                snake[0][1] + Directions[currentDirection][1]]  # advance the head in the current direction


'''
    :argument snake is a list of tails, including the head
    :argument apple is the position of the current apple in the game
    :argument stepsTaken is the amount of steps already taken, this will not be modified by checkRules
        also automatically extends the snake and give apple a new position if the snake has eaten an apple
    :returns False if any rule is broken, otherwise True
'''


def checkRules(snake=None, apple=None, stepsTakenSinceApple=None, mute=True):
    retString = 'Rules Followed'
    if stepsTakenSinceApple > StepsUntilStarve:
        if not mute:
            print('starved')
        return None
    if BoardSize[0] <= snake[0][0] or snake[0][0] < 0 or BoardSize[1] <= snake[0][1] or snake[0][1] < 0:  # Boundary check
        if not mute:
            print('hit wall')
        return None
    if apple == snake[0]:  # Apple check
        snake.append([-1, -1])
        newPos = generateApplePos(snake)
        apple[0] = newPos[0]
        apple[1] = newPos[1]
        retString = 'Apple'
    for i in range(len(snake)):  # Self hit check
        for j in range(len(snake)):
            if not j == i:
                if not snake[i] == [-1, -1] and not snake[j] == [-1, -1] and snake[i] == snake[j]:  # ignore tail pieces with [-1, -1] (used for init)
                    if not mute:
                        print('hit self=> ', i, ':', snake[i], ' = ', j, ':', snake[j])
                    return None
    return retString


'''
:argument controller is a controller that will be used for getting the next direction
:returns snake, SnakeInitSize, stepsTaken
'''


def runForFitness(controller):
    currentDirection = "North"  # init currentDirection
    stepsTaken = 0  # init a counter to keep track of the amount of steps taken
    stepsTakenSinceApple = 0
    snake = [[int(np.round(BoardSize[0]/2)), int(np.round(BoardSize[1]/2))]]  # set the starting point
    for i in range(SnakeInitSize - 1):  # add tail pieces, [-1, -1] is for all intents and purposes non initialized
        snake.append([-1, -1])
    apple = generateApplePos(snake)  # init apple to a random point
    rulesRes = True
    while rulesRes:
        rulesRes = checkRules(snake, apple, stepsTakenSinceApple)
        currentDirection = controller.nextDir(BoardSize, snake, apple, currentDirection)
        advanceSnake(snake, currentDirection)
        stepsTaken += 1
        stepsTakenSinceApple += 1
        if rulesRes == 'Apple':
            stepsTakenSinceApple = 0
    return snake, SnakeInitSize, stepsTaken


'''
a class that'll take a tkinter canvas, a controller and the size specs of the given canvas, it'll then play and draw a game
tick every time stepAndDraw is called, which'll return whether or not any rules are broken
'''


class ControllerPreview:
    def __init__(self, controller, canvas, CanvasSize, netCanvas=None):
        self.canvas = canvas
        self.netCanvas = netCanvas
        self.CanvasSize = CanvasSize
        self.blockSize = np.min(CanvasSize) / np.max(BoardSize)

        self.controller = controller
        self.snake = [[int(np.round(BoardSize[0]/2)), int(np.round(BoardSize[1]/2))]]   # set the starting point
        self.stepsTaken = 0  # init a counter to keep track of the amount of steps taken
        self.stepsTakenSinceApple = 0
        for i in range(SnakeInitSize - 1):  # add tail pieces, [-1, -1] is for all intents and purposes non initialized
            self.snake.append([-1, -1])

        self.currentDirection = "North"  # init currentDirection
        self.apple = generateApplePos(self.snake)  # init apple to a random point

    def stepAndDraw(self):
        if self.netCanvas:
            self.currentDirection, activations = self.controller.nextDir(BoardSize, self.snake.copy(), self.apple, self.currentDirection, fetchActivations=True)
        else:
            self.currentDirection = self.controller.nextDir(BoardSize, self.snake.copy(), self.apple, self.currentDirection)
        advanceSnake(self.snake, self.currentDirection)
        self.stepsTaken += 1
        self.stepsTakenSinceApple += 1

        rulesRes = checkRules(self.snake, self.apple, self.stepsTakenSinceApple, mute=True)
        if rulesRes:
            self.drawGame()
            if self.netCanvas:
                self.drawNet(activations, self.netCanvas, self.controller.brain.layers)
            if rulesRes == 'Apple':
                self.stepsTakenSinceApple = 0
            return True
        return False

    def reset(self, newController):
        self.snake = [[int(np.round(BoardSize[0]/2)), int(np.round(BoardSize[1]/2))]]   # set the starting point
        for i in range(SnakeInitSize - 1):  # add tail pieces, [-1, -1] is for all intents and purposes non initialized
            self.snake.append([-1, -1])
        self.controller = newController
        self.currentDirection = "North"  # reset currentDirection
        self.apple = generateApplePos(self.snake)  # reset apple to a random point
        self.stepsTaken = 0
        self.stepsTakenSinceApple = 0

    def __drawBox__(self, x, y, color):
        if not x == -1 and not y == -1:
            self.canvas.create_rectangle(x * self.blockSize, y * self.blockSize,
                                         (x + 1) * self.blockSize, (y + 1) * self.blockSize,
                                         fill=color)

    def drawGame(self):
        self.canvas.create_rectangle(0, 0, self.CanvasSize[0], self.CanvasSize[1], fill='light grey')
        self.__drawBox__(self.snake[0][0], self.snake[0][1], 'dark green')
        for i in range(1, len(self.snake)):
            self.__drawBox__(self.snake[i][0], self.snake[i][1], 'forest green')
        self.__drawBox__(self.apple[0], self.apple[1], 'red')


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
        xPadding = 40
        layerXPos = (netCanvas.winfo_width() - xPadding * 2) / (layerCount - 1)

        # largest y offset found to create the largest orb size possible while still fitting in all the orbs in every layer
        largestLayerYPos = netCanvas.winfo_height() / (largestColumn + 1)
        orbsSize = min(layerXPos, largestLayerYPos) / 1.1

        layerYPos = []
        # get the y offset for each orb in layer i to space them evenly
        for i in range(layerCount):
            layerYPos.append(netCanvas.winfo_height() / (len(activations[i]) + 1))

        getOrbPos = lambda layer, weightIndex: \
            (xPadding + layer * layerXPos - (orbsSize / 2),
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
                fill = ""
                # activationStrength is calculated as a percentage of the largest activation
                nodeActivationStrength = int(np.round(255 * (activations[i][j] / np.max(activations[i]))))
                if j == len(activations[i]) - 1 and i != layerCount - 1:
                    fill = ColorFromrgb((0, 0, nodeActivationStrength))
                else:
                    fill = ColorFromrgb((nodeActivationStrength, 0, nodeActivationStrength))

                orbPos = getOrbPos(i, j)
                # if it's the highest up node it gets blue to indicate the fact
                drawCircle(
                    (orbPos[0] - orbsSize / 2, orbPos[1] - orbsSize / 2),
                    fill,
                    orbsSize, netCanvas)
