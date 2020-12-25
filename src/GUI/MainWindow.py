import tkinter as tk
import numpy as np
import SnakeEngine.SnakeRunner as SnakeRunner
import GUI.SnakeManager as SnakeManager
import threading

# config
CanvasSize = [400, 400]
NetCanvasSize = [600, 600]
MovesPerSecond = 10


class MainWindow(tk.Tk):

    def __init__(self, showNet=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainCanvas = tk.Canvas(width=CanvasSize[0], height=CanvasSize[1], borderwidth=0, highlightthickness=0)
        self.mainCanvas.grid(row=0, column=0)
        self.infoLabel = tk.Label(text='')
        self.infoLabel.grid(row=1, column=0)
        if showNet:
            self.netCanvas = tk.Canvas(width=NetCanvasSize[0], height=NetCanvasSize[1],  borderwidth=0, highlightthickness=0)
            self.netCanvas.grid(row=0, column=1, rowspan=2)
        else:
            self.netCanvas = None


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

    mw = MainWindow(True)
    manager = SnakeManager.SnakeManager()
    mc = ManualController(mw)
    controlPreview = SnakeRunner.ControllerPreview(manager.bestSnake, mw.mainCanvas, CanvasSize, mw.netCanvas)
    mw.infoLabel.config(text='Generation: 0 || best fitness: 0')


    def stepAndDrawLoop():
        if not controlPreview.stepAndDraw():
            bestSnake = manager.bestSnake
            controlPreview.reset(bestSnake)
            mw.infoLabel.config(text='Generation: ' + str(manager.generation - 1) + ' || best fitness: ' + str(bestSnake.getFitness()))
        mw.mainCanvas.after(int(np.round(1000 / MovesPerSecond)), stepAndDrawLoop)


    mw.after(1, stepAndDrawLoop)
    t = threading.Thread(target=manager.runPopulation)
    t.setDaemon(True)
    t.start()
    mw.mainloop()
