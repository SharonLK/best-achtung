from action import Action
from board import Board
from players.player import Player

import random


class RandomPlayer(Player):

    def move(self, board: Board, keys) -> Action:

        x = random.random()
        return Action.Right if x < 0.01 else Action.Left if x < 0.02 else Action.Stand
