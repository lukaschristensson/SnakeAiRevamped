import tkinter as tk
import numpy as np
import SnakeEngine.SnakeManager as SnakeManager
import CrappyBird.BirdManager as BirdManager
import CrappyBird.BirdRunner as BirdRunner
import threading
import time

# config
CanvasSize = [400, 400]
NetCanvasSize = [600, 600]


def updateLabel():
    if MainWindow.InfoLabel:
        finalString = ''
        for i in range(len(MainWindow.InfoLabelText)):
            if i != 0:
                finalString += ' || '
            finalString += MainWindow.InfoLabelText[i]
        MainWindow.InfoLabel.config(text=finalString)


class MainWindow(tk.Tk):
    MovesPerSecond = 30
    InfoLabelText = []
    killBird = False

    def __init__(self, showNet=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainCanvas = tk.Canvas(width=CanvasSize[0], height=CanvasSize[1], borderwidth=0, highlightthickness=0)
        self.mainCanvas.grid(row=0, column=0)
        self.infoLabel = tk.Label(text='')
        self.infoLabel.grid(row=1, column=0)
        MainWindow.InfoLabel = self.infoLabel
        if showNet:
            self.netCanvas = tk.Canvas(width=NetCanvasSize[0], height=NetCanvasSize[1], borderwidth=0,
                                       highlightthickness=0)
            self.netCanvas.grid(row=0, column=1, rowspan=2)
        else:
            self.netCanvas = None

        def plusMPS(event):
            MainWindow.MovesPerSecond += 1
            if MainWindow.InfoLabelText and len(MainWindow.InfoLabelText) > 1:
                MainWindow.InfoLabelText[2] = 'MPS: ' + str(MainWindow.MovesPerSecond)
                updateLabel()

        def minusMPS(event):
            MainWindow.MovesPerSecond -= 1
            if MainWindow.InfoLabelText and len(MainWindow.InfoLabelText) > 1:
                MainWindow.InfoLabelText[2] = 'MPS: ' + str(MainWindow.MovesPerSecond)
                updateLabel()

        def kill(event):
            MainWindow.killBird = True

        self.bind('k', kill)
        self.bind('w', plusMPS)
        self.bind('s', minusMPS)



class ManualController:

    def __init__(self, mainWindow):
        self.presetDirection = "North"
        self.jump = False
        self.hasReleased = True

        def setDirection(direction):
            self.presetDirection = direction

        def setReleased():
            self.hasReleased = True

        def preloadJump():
            if self.hasReleased:
                self.jump = True
                self.hasReleased = False

        mainWindow.bind('<Left>', lambda event: setDirection('West'))
        mainWindow.bind('<Right>', lambda event: setDirection('East'))
        mainWindow.bind('<Up>', lambda event: setDirection('North'))
        mainWindow.bind('<Down>', lambda event: setDirection('South'))
        mainWindow.bind('<space>', lambda event: preloadJump())
        mainWindow.bind('<KeyRelease-space>', lambda event: setReleased())

    def nextDir(self, BoardSize, snake, apple, currentDirection):
        return self.presetDirection

    def getJump(self, pillars, birdPos, verticalVelocity):
        if self.jump:
            self.jump = False
            return True
        else:
            return False


if __name__ == '__main__':

    mw = MainWindow(True)
    mc = ManualController(mw)

    snakeManager = SnakeManager.SnakeManager()
    birdManager = BirdManager.BirdManager()
    # snakeControlPreview = SnakeRunner.ControllerPreview(snakeManager.bestSnake, mw.mainCanvas, CanvasSize, mw.netCanvas)
    MainWindow.InfoLabelText.append('Generation: 0')
    MainWindow.InfoLabelText.append('best fitness: 0')
    MainWindow.InfoLabelText.append('MPS: ' + str(MainWindow.MovesPerSecond))

    birdControlPreview = BirdRunner.ControllerReview(birdManager.bestBird, mw.mainCanvas, CanvasSize, mw.netCanvas)
    MainWindow.InfoLabelText.append('Score: ' + str(birdControlPreview.score))

    # def snakeStepAndDrawLoop():
    #    startTime = time.time()
    #    if not snakeControlPreview.stepAndDraw():
    #        bestSnake = snakeManager.bestSnake
    #        snakeControlPreview.reset(bestSnake)
    #        mw.infoLabel.config(text=
    #                            'Generation: ' + str(snakeManager.generation) + ' || ' +
    #                            'best fitness: ' + str(np.round(bestSnake.getFitness()))
    #                            )
    #    msForFrame = int((time.time() - startTime) * 1000)
    #    mw.mainCanvas.after(np.maximum(msBetweenFrames - msForFrame, 1), snakeStepAndDrawLoop)

    def birdStepAndDrawLoop(killBird=None):
        startTime = time.time()
        msBetweenFrames = int(np.round(1000 / MainWindow.MovesPerSecond))

        MainWindow.InfoLabelText[3] = 'Score: ' + str(birdControlPreview.score)
        updateLabel()

        if not birdControlPreview.stepAndDraw() or MainWindow.killBird:
            bestBird = birdManager.bestBird
            birdControlPreview.reset(bestBird)
            MainWindow.InfoLabelText[0] = 'Generation: ' + str(birdManager.generation)
            MainWindow.InfoLabelText[1] = 'best fitness: ' + str(np.round(bestBird.getFitness()))
            MainWindow.killBird = False
        msForFrame = int((time.time() - startTime) * 1000)
        mw.mainCanvas.after(np.maximum(msBetweenFrames - msForFrame, 1), birdStepAndDrawLoop, killBird)


    # mw.after(1, snakeStepAndDrawLoop)
    snakeT = threading.Thread(target=snakeManager.runPopulation)
    snakeT.setDaemon(True)
    # snakeT.start()
    mw.after(1, birdStepAndDrawLoop)
    birdT = threading.Thread(target=birdManager.runPopulation)
    birdT.setDaemon(True)
    birdT.start()

    mw.mainloop()
