from view import GuiView
from game_sever import GameServer
import lib
import socket


class Controller:
    def __init__(self):
        self.view = GuiView(self)
        self.socket = None
        self.mark = None
        self.other_player_name = None
        self.instruction = None

    def start(self):
        self.view.start()

    def connect(self, name, ip):
        print(f"This is {name}")
        self.socket = socket.socket()
        self.socket.connect((ip, GameServer.PORT))
        self.mark = self.socket.recv(4096).decode()
        print(f"{self.mark} received")
        self.socket.send(name.encode())
        self.view.show_waiting()
        self.other_player_name = self.socket.recv(4096).decode()
        print(f"{self.other_player_name} joined")
        self.view.show_board()
        self.socket.send("ACK".encode())
        self.handle_next_instruction()

    def handle_next_instruction(self):
        print("Waiting for instruction...")
        self.instruction = self.socket.recv(4096).decode()
        print(f"Instruction: {self.instruction}")
        if self.instruction == "turn":
            self.view.show_turn_instruction()
        elif self.instruction == "waiting":
            self.view.wait_for_other_player(self.other_player_name)
            fieldnumber = int(self.socket.recv(4096).decode())
            print(fieldnumber)
            if self.mark == lib.PLAYER_1_MARK:
                mark_other_player = lib.PLAYER_2_MARK
            else:
                mark_other_player = lib.PLAYER_1_MARK
            self.view.update_board(fieldnumber, mark_other_player)
            self.socket.send("ACK".encode())
            print("ack sent")
            self.handle_next_instruction()
        elif self.instruction == "Winner":
            self.socket.send("ACK".encode())
            winner_name = self.socket.recv(4096).decode()
            if winner_name == self.other_player_name:
                self.view.show_winner_text(f"{winner_name} wins!")
            else:
                self.view.show_winner_text(f"You win!")
        elif self.instruction == "Draw":
            self.view.show_draw()
        else:
            self.view.show_input_error()

    def send_field_number(self, field_number):
        if self.instruction == "turn":
            self.view.update_board(field_number, self.mark)
            self.socket.send(str(field_number).encode())
            print(f"Field number {field_number} sent.")
            self.handle_next_instruction()
