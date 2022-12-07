import socket
from game import Game
from lib import *


class GameServer():
    # Standard loopback interface address (localhost)
    HOST = ""
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
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((GameServer.HOST, GameServer.PORT))
            s.listen()
            print("Tic-Tac-Toe-Server is listening...")
            self.client_connection_1, address_1 = s.accept()
            self.client_connection_1.send(PLAYER_1_MARK.encode())
            player_name_1 = self.client_connection_1.recv(4096).decode()
            print(f"Player 1 ({player_name_1} at {address_1}) connected.")

            self.client_connection_2, address_2 = s.accept()
            self.client_connection_2.send(PLAYER_2_MARK.encode())
            player_name_2 = self.client_connection_2.recv(4096).decode()
            print(f"Player 2 ({player_name_2} at {address_1} connected.")

            print("Send joined player names")
            self.client_connection_1.send(player_name_2.encode())
            self.client_connection_2.send(player_name_1.encode())

            ack_player_1 = self.client_connection_1.recv(4096).decode()
            print(f"Player 1: {ack_player_1}")
            ack_player_2 = self.client_connection_2.recv(4096).decode()
            print(f"Player 2: {ack_player_2}")

            print("Preparing game...")
            self.game.prepare(player_name_1, player_name_2)

            counter = 1
            while not self.game.is_finished:
                print(f"Round: {counter}")
                if self.game.active_player == self.game.player_1:
                    print("Sending instructions...")
                    print("Player 1 turn")
                    print("Player 2 waiting")
                    self.client_connection_1.send("turn".encode())
                    self.client_connection_2.send("waiting".encode())
                    print("Waiting for field")
                    field_number = int(self.client_connection_1.recv(4096).decode())
                    print(f"Field number {field_number} received.")
                    if self.game.board.can_place(field_number):
                        self.game.make_a_turn(field_number)
                        print(f"Send {field_number} to player 2")
                        self.client_connection_2.send(f"{field_number}".encode())
                        print(f"Waiting for ACK from player 2...")
                        ack = self.client_connection_2.recv(4096).decode()
                        print(f"Player 2: {ack}.")
                else:
                    print("Sending instructions...")
                    print("Player 1 waiting")
                    print("Player 2 turn")
                    self.client_connection_1.send("waiting".encode())
                    self.client_connection_2.send("turn".encode())
                    print("Waiting for field")
                    field_number = int(self.client_connection_2.recv(4096).decode())
                    print(f"Field number {field_number} received.")
                    if self.game.board.can_place(field_number):
                        self.game.make_a_turn(field_number)
                        print(f"Send {field_number} to player 1")
                        self.client_connection_1.send(f"{field_number}".encode())
                        print(f"Waiting for ACK from player 1...")
                        ack = self.client_connection_1.recv(4096).decode()
                        print(f"Player 1: {ack}.")
                self.game.change_active_player()
                counter += 1
            if self.game.board.has_winner():
                winner_name = self.game.get_winner_name()
                print(f"Finished. Winner: {winner_name}")
                self.client_connection_1.send(f"Winner".encode())
                self.client_connection_2.send(f"Winner".encode())
                ack_player_1 = self.client_connection_1.recv(4096).decode()
                print(f"Player 1: {ack_player_1}")
                ack_player_2 = self.client_connection_2.recv(4096).decode()
                print(f"Player 2: {ack_player_2}")
                self.client_connection_1.send(f"{winner_name}".encode())
                self.client_connection_2.send(f"{winner_name}".encode())
            else:
                print("Draw")
                self.client_connection_1.send(f"Draw".encode())
                self.client_connection_2.send(f"Draw".encode())
