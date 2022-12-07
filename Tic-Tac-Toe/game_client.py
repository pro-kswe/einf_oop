from controller import Controller


class GameClient():
    def __init__(self):
        self.controller = Controller()

    def start(self):
        self.controller.start()
