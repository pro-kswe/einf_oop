from view import GuiView
from game_sever import GameServer
import lib
import socket


class Controller:
    def __init__(self):
        self.view = GuiView(self)
        self.socket = None
        self.mark = None

    def start(self):
        self.view.start()

    def connect(self, name, ip):
        self.socket = socket.socket()
        self.socket.connect((ip, GameServer.PORT))
        self.mark = self.socket.recv(4096).decode()
        print(f"{self.mark} received")
        self.socket.send(name.encode())
        self.view.show_waiting()
        name = self.socket.recv(4096).decode()
        print(f"{name} joined")

    def start_game(self, name):
        print("Waiting for another player...")
        self.view.show_board()
        self.handle_next_instruction()

    def handle_next_instruction(self):
        instruction = self.socket.recv(4096).decode()
        if instruction == "turn":
            self.view.show_turn_instruction()
        else:
            self.view.show_waiting_instruction()
            fieldnumber = int(self.socket.recv(4096).decode())
            if self.mark == lib.PLAYER_1_MARK:
                mark_other_player = lib.PLAYER_2_MARK
            else:
                mark_other_player = lib.PLAYER_1_MARK
            self.view.update_board(fieldnumber, mark_other_player)

    def sendFieldNumber(self, field_number):
        self.view.update_board(field_number, self.mark)
        self.socket.send(str(field_number).encode())
