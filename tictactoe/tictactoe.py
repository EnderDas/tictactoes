import time

class TicTacToe:

    def __init__(self, parent):
        self.parent = parent
        self.screen = self.parent.screen
        self.input = self.parent.input
        self.inp_handle = self.parent.inp_handle

    def GameLoop(self):
        self.screen.clear()
        self.screen.printAtCenter("Not available yet sorry!")
        time.sleep(5)
        self.parent.Quit()

class ChaosTtt:

    def __init__(self, parent):
        self.parent = parent
        self.screen = self.parent.screen
        self.input = self.parent.input
        self.inp_handle = self.parent.inp_handle

    def GameLoop(self):
        self.screen.clear()
        self.screen.printAtCenter("Not available yet sorry!")
        time.sleep(5)
        self.parent.Quit()

class PandemoniumTtt:

    def __init__(self, parent):
        self.parent = parent
        self.screen = self.parent.screen
        self.input = self.parent.input
        self.inp_handle = self.parent.inp_handle

    def GameLoop(self):
        self.screen.clear()
        self.screen.printAtCenter("Not available yet sorry!")
        time.sleep(5)
        self.parent.Quit()

