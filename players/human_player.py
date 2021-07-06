import pygame

from action import Action
from board import Board
from head import Head
from players.player import Player


class HumanPlayer(Player):

    def __init__(self, head: Head, left_key, right_key):
        super().__init__(head)

        self.left_key = left_key
        self.right_key = right_key

    def move(self, board: Board, events) -> Action:

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == self.left_key:
                    return Action.Left
                if event.key == self.right_key:
                    return Action.Right

        return Action.Stand
