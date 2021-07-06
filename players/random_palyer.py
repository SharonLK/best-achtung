import random

from action import Action
from board import Board
from players.player import Player


class RandomPlayer(Player):
    def move(self, board: Board, event=None) -> Action:
        x = random.random()
        return Action.Right if x < 0.3 else Action.Left if x < 0.06 else Action.Stand
