from abc import ABC, abstractmethod

from action import Action
from board import Board
from head import Head


class Player(ABC):

    def __init__(self, head: Head):
        self.head = head

    @abstractmethod
    def move(self, board: Board, event) -> Action:
        pass
