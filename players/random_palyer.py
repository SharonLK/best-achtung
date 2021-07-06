from action import Action
from board import Board
from players.player import Player

import random


class RandomPlayer(Player):

    def move(self, board: Board, event) -> Action:

        x = random.random()
        return Action.Right if x < 0.2 else Action.Left if x < 0.4 else Action.Stand
