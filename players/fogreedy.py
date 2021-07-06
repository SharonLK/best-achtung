from action import Action
from board import Board
from players.player import Player
import numpy as np
import random

BORDERS_BUFFER = 5
STEP = 3
DIRECTIONS = {'s': 0,
              'se': np.pi / 4,
              'e': np.pi / 2,
              'ne': 3 * np.pi / 4,
              'n': np.pi,
              'nw': 5 * np.pi / 4,
              'w': 3 * np.pi / 2,
              'sw': 7 * np.pi / 4}


class Fogreedy(Player):
    def __init__(self, head):
        super().__init__(head)
        self.border_buffer = BORDERS_BUFFER
        self.counter = 0

    def move(self, board: Board, keys=None) -> Action:
        r = self.head.x
        c = self.head.y

        self.counter += 1

        if r < self.border_buffer:
            self.head.direction = DIRECTIONS['se']
            return Action.Stand
        elif c < self.border_buffer:
            self.head.direction = DIRECTIONS['se']
            return Action.Stand
        elif r > board.height - self.border_buffer:
            self.head.direction = DIRECTIONS['nw']
            return Action.Stand
        elif c > board.width - self.border_buffer:
            self.head.direction = DIRECTIONS['nw']
            return Action.Stand

        x = random.random()

        return Action.Right if x < 0.5 else Action.Left
