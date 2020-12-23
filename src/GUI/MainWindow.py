import tkinter as tk
import numpy as np
import src.SnakeEngine.SnakeRunner as SnakeRunner
import NeuralNet.Network as Network
import GeneticAlgorithm.CrossOver as CrossOver


# config
CanvasSize = [400, 400]
MovesPerSecond = 5


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainCanvas = tk.Canvas(width=CanvasSize[0], height=CanvasSize[1])
        self.mainCanvas.grid(row=0, column=0)


class ManualController:

    def __init__(self, mainWindow):
        self.presetDirection = "North"

        def setDirection(direction):
            self.presetDirection = direction

        mainWindow.bind('<Left>', lambda event: setDirection('West'))
        mainWindow.bind('<Right>', lambda event: setDirection('East'))
        mainWindow.bind('<Up>', lambda event: setDirection('North'))
        mainWindow.bind('<Down>', lambda event: setDirection('South'))

    def nextDir(self, BoardSize, snake, apple, currentDirection):
        return self.presetDirection


if __name__ == '__main__':
    nn1 = Network.NeuralNetwork([40, 10, 25, 4])
    nn2 = Network.NeuralNetwork([40, 10, 25, 4])
    # print(nn.feedForward(np.random.uniform(0, 3, (1, 40))))

    CrossOver.nPointCrossover(nn1, nn2, 2)
    mw = MainWindow()
    controlPreview = SnakeRunner.ControllerPreview(ManualController(mw), mw.mainCanvas, CanvasSize)


    def stepAndDrawLoop():
        if controlPreview.stepAndDraw():
            mw.mainCanvas.after(int(np.round(1000 / MovesPerSecond)), stepAndDrawLoop)


    stepAndDrawLoop()
    mw.mainloop()
