from typing import List, Optional

import numpy as np
import pygame
from constants import *

from action import Action
from board import Board
from head import Head


def as_int(pos: np.ndarray) -> List[int]:
    return [int(pos[0]), int(pos[1])]


def draw_player(color, center, surface):
    pygame.draw.circle(surface, color, center, RADIUS)


def draw_path(path, screen, color):
    for point in path:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], PATH_RADIUS)


class Game:
    def __init__(self):

        self.board: Optional[Board] = None
        self.head1: Optional[Head] = None
        self.head2: Optional[Head] = None
        self.winner: Optional[int] = None
        self.screen: Optional = None
        self.empty: Optional[bool] = False
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
        self.head1 = Head(pos1, direction1, SPEED)

        pos2 = self._choose_initial_pos()
        direction2 = self._choose_initial_angle(pos1)
        self.head2 = Head(pos2, direction2, SPEED)

        while self.head1.distance(self.head2) < 100:
            pos1 = self._choose_initial_pos()
            direction1 = self._choose_initial_angle(pos1)
            self.head1 = Head(pos1, direction1, SPEED)

            pos2 = self._choose_initial_pos()
            direction2 = self._choose_initial_angle(pos1)
            self.head2 = Head(pos2, direction2, SPEED)

        self.ended = False
        self.winner = None
        self.empty = False

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)

    @staticmethod
    def _move_head(head: Head, action: Action) -> None:
        if action == Action.Right:
            head.change_direction(-DTHETA)
        elif action == Action.Left:
            head.change_direction(DTHETA)

        head.step()

    def advance(self, action1: Action, action2: Action) -> None:
        self.time += 1

        if self.empty:
            draw_player(BLACK, as_int(self.head1.pos), self.screen)
            draw_player(BLACK, as_int(self.head2.pos), self.screen)
        else:
            draw_player(p1_path_color, as_int(self.head1.pos), self.screen)
            draw_player(p2_path_color, as_int(self.head2.pos), self.screen)

        self._move_head(self.head1, action1)
        self._move_head(self.head2, action2)

        draw_player(p1_color, as_int(self.head1.pos), self.screen)
        draw_player(p2_color, as_int(self.head2.pos), self.screen)

        pygame.display.flip()

        self.empty = self.time % cycle_time > cycle_time - empty_time

        if not self.board.legal_pos(self.head1.pos):
            print('Player 1 has lost')
            self.ended = True
            self.winner = 2
            return

        if not self.board.legal_pos(self.head2.pos):
            print('Player 2 has lost')
            self.ended = True
            self.winner = 1
            return

        if not self.empty:
            self.board.update_occupancy(self.head1.pos, self.head2.pos)
        else:
            self.board.update_occupancy()

    def has_ended(self) -> bool:
        return self.ended

    def end(self) -> None:
        self.ended = True
