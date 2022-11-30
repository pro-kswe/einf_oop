from board import Board
import random as r
from player import Player
from lib import *


class Game:
    def __init__(self):
        self.board = Board()
        self.player_1 = None
        self.player_2 = None
        self.active_player = None
        self.is_finished = False

    def prepare(self, player_1_name, player_2_name):
        self.player_1 = Player(player_1_name, PLAYER_1_MARK)
        self.player_2 = Player(player_2_name, PLAYER_2_MARK)
        self.active_player = r.choice([self.player_1, self.player_2])

    def change_active_player(self):
        if self.active_player == self.player_1:
            self.active_player = self.player_2
        else:
            self.active_player = self.player_1

    def make_a_turn(self, position):
        self.board.place(position, self.active_player)
        self.board.determine_winner()
        if self.board.has_winner() or self.board.is_draw():
            self.is_finished = True
