from typing import Optional
import numpy as np

from action import Action
from board import Board
from head import Head

speed = 0.15
dtheta = 0.3

radius = 5
path_radius = 5

cycle_time = 1500
empty_time = 150


class Game:

    def __init__(self):

        self.board: Optional[Board] = None
        self.head1: Optional[Head] = None
        self.head2: Optional[Head] = None
        self.time = 0

        self.reset()

        self.ended = False

    def _choose_initial_pos(self):
        return (np.random.uniform(low=0.25, high=0.75, size=2) * np.array(
            [self.board.width, self.board.height])).astype(int)

    def _choose_initial_angle(self, pos: np.ndarray):
        if pos[0] < self.board.width / 2 and pos[1] < self.board.height / 2:
            angle = 0.25 * np.pi
        elif pos[0] < self.board.width / 2 and pos[1] > self.board.height / 2:
            angle = 0.75 * np.pi
        elif pos[0] > self.board.width / 2 and pos[1] > self.board.height / 2:
            angle = 1.25 * np.pi
        else:
            angle = 1.75 * np.pi

        return angle + np.pi * np.random.uniform(low=-0.25, high=0.25)

    def reset(self) -> None:

        self.time = 0

        self.board = Board()

        pos1 = self._choose_initial_pos()
        direction1 = self._choose_initial_angle(pos1)
        self.head1 = Head(pos1, direction1, speed)

        pos2 = self._choose_initial_pos()
        direction2 = self._choose_initial_angle(pos1)
        self.head2 = Head(pos2, direction2, speed)

        while self.head1.distance(self.head2) < 100:
            pos1 = self._choose_initial_pos()
            direction1 = self._choose_initial_angle(pos1)
            self.head1 = Head(pos1, direction1, speed)

            pos2 = self._choose_initial_pos()
            direction2 = self._choose_initial_angle(pos1)
            self.head2 = Head(pos2, direction2, speed)

        self.ended = False

    @staticmethod
    def _move_head(head: Head, action: Action) -> None:
        if action == Action.Right:
            head.change_direction(-dtheta)
        elif action == Action.Left:
            head.change_direction(dtheta)

        head.step()

    def advance(self, action1: Action, action2: Action) -> bool:

        self.time += 1

        self._move_head(self.head1, action1)
        self._move_head(self.head2, action2)

        empty = self.time % cycle_time > cycle_time - empty_time

        if not self.board.legal_pos(self.head1.pos):
            print('Player 1 has lost')
            self.ended = True
            return empty

        if not self.board.legal_pos(self.head2.pos):
            print('Player 2 has lost')
            self.ended = True
            return empty

        if not empty:
            self.board.update_occupancy(self.head1.pos, self.head2.pos)
        else:
            self.board.update_occupancy()

        return empty

    def has_ended(self) -> bool:
        return self.ended

    def end(self) -> None:
        self.ended = True
