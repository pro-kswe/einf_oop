from controller import Controller
import socket
from game_sever import GameServer


class GameClient():
    def __init__(self):
        self.controller = Controller()

    def start(self):
        ip = input("IP? ")
        with socket.socket() as s:
            s.connect((ip, GameServer.PORT))
            self.controller.start(s)


