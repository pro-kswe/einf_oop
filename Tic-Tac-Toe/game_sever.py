import socket
from game import Game
from lib import *


class GameServer():
    # Standard loopback interface address (localhost)
    HOST = "127.0.0.1"
    PORT = 42420

    def __init__(self):
        self.game = Game()
        self.client_connection_1 = None
        self.client_connection_2 = None

    def start(self):
        print("Tic-Tac-Toe-Server is running...")
        # AF_INET: IP v4
        # SOCK_STREAM: TCP
        with socket.socket() as s:
            s.bind((GameServer.HOST, GameServer.PORT))
            s.listen()
            self.client_connection_1, address_1 = s.accept()
            print(f"Player 1 at {address_1} connected.")
            self.client_connection_1.send(PLAYER_1_MARK.encode())
            player_name_1 = self.client_connection_1.recv(4096).decode()
            print(player_name_1)

            self.client_connection_2, address_2 = s.accept()
            print(f"Player 2 at {address_2} connected.")
            self.client_connection_2.send(PLAYER_2_MARK.encode())
            player_name_2 = self.client_connection_2.recv(4096).decode()
            print(player_name_2)

            self.game.prepare(player_name_1, player_name_2)

            self.client_connection_1.send(self.game.player_2.name.encode())
            self.client_connection_2.send(self.game.player_1.name.encode())

            while not self.game.is_finished:
                if self.game.active_player == self.game.player_1:
                    self.client_connection_1.send("turn".encode())
                    self.client_connection_2.send("waiting".encode())
                    field_number = int(self.client_connection_1.recv(4096).decode())
                    if self.game.board.can_place(field_number):
                        self.game.make_a_turn(field_number)
                        self.client_connection_2.send("field_number".encode())
                else:
                    self.client_connection_1.send("waiting".encode())
                    self.client_connection_2.send("turn".encode())
                    field_number = int(self.client_connection_2.recv(4096).decode())
                    if self.game.board.can_place(field_number):
                        self.game.make_a_turn(field_number)
                        self.client_connection_1.send("field_number".encode())
                    self.game.change_active_player()
            if self.game.board.has_winner():
                print("Winner")
            else:
                print("Draw")
