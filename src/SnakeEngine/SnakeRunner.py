import numpy as np

# config
BoardSize = [20, 20]
SnakeInitSize = 3
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


def checkRules(snake=None, apple=None, stepsTakenSinceApple=None):
    retString = 'Rules Followed'
    if stepsTakenSinceApple > StepsUntilStarve:
        return None
    if BoardSize[0] < snake[0][0] or snake[0][0] < 0 or BoardSize[1] < snake[0][1] or snake[0][1] < 0:  # Boundary check
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
    snake = [[np.default_rng() * BoardSize[0], np.default_rng() * BoardSize[1]]]  # set a random starting point
    for i in range(SnakeInitSize):  # add tail pieces, [-1, -1] is for all intents and purposes non initialized
        snake.append([-1, -1])
    apple = generateApplePos(snake)  # init apple to a random point
    rulesRes = True
    while rulesRes:
        rulesRes = checkRules(snake, apple)
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
    def __init__(self, controller, canvas, CanvasSize):
        self.controller = controller
        self.canvas = canvas
        self.CanvasSize = CanvasSize
        self.blockSize = np.min(CanvasSize) / np.max(BoardSize)
        self.snake = [[int(np.round(BoardSize[0]/2)), int(np.round(BoardSize[1]/2))]]   # set the starting point
        self.stepsTaken = 0  # init a counter to keep track of the amount of steps taken
        self.stepsTakenSinceApple = 0
        for i in range(SnakeInitSize):  # add tail pieces, [-1, -1] is for all intents and purposes non initialized
            self.snake.append([-1, -1])

        self.currentDirection = "North"  # init currentDirection
        self.apple = generateApplePos(self.snake)  # init apple to a random point

    def stepAndDraw(self):
        self.currentDirection = self.controller.nextDir(BoardSize, self.snake, self.apple, self.currentDirection)
        advanceSnake(self.snake, self.currentDirection)
        self.stepsTaken += 1
        self.stepsTakenSinceApple += 1

        rulesRes = checkRules(self.snake, self.apple, self.stepsTaken)
        if rulesRes:
            print(self.stepsTakenSinceApple)
            self.drawGame()
            if rulesRes == 'Apple':
                self.stepsTakenSinceApple = 0
            return True
        return False

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
