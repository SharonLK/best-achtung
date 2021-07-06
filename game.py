from typing import List, Optional

import numpy as np
import pygame

from action import Action
from board import Board
from head import Head

speed = 10
dtheta = 0.3

radius = 5
path_radius = 5

cycle_time = 120 // speed
empty_time = 20 // speed

screen_size = (800, 600)

marker_colors = [(255, 255, 255), (0, 255, 255)]
path_colors = [(255, 255, 0), (255, 0, 255)]

BLACK = (0, 0, 0)


def as_int(pos: np.ndarray) -> List[int]:
    return [int(pos[0]), int(pos[1])]


def draw_player(color, center, surface):
    pygame.draw.circle(surface, color, center, radius)


def draw_path(path, screen, color):
    for point in path:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], path_radius)


class Game:
    def __init__(self, n: int):

        self.n = n
        self.marker_colors = marker_colors[:self.n]
        self.path_colors = path_colors[:self.n]

        self.board: Optional[Board] = None
        self.heads: Optional[List[Head]] = None
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

        self.heads = []
        for _ in range(self.n):
            pos = self._choose_initial_pos()
            direction = self._choose_initial_angle(pos)
            head = Head(pos, direction, speed)
            self.heads.append(head)

        self.ended = False
        self.empty = False

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)

    @staticmethod
    def _move_head(head: Head, action: Action) -> List[np.ndarray]:
        if action == Action.Right:
            head.change_direction(-dtheta)
        elif action == Action.Left:
            head.change_direction(dtheta)

        return head.step()

    def advance(self, action1: Action) -> None:
        self.time += 1

        for head, color in zip(self.heads, self.path_colors):
            if self.empty:
                draw_player(BLACK, as_int(head.pos), self.screen)
            else:
                draw_player(color, as_int(head.pos), self.screen)

        visited = []
        for head, color in zip(self.heads, self.marker_colors):
            visited += self._move_head(head, action1)
            draw_player(color, as_int(head.pos), self.screen)

        pygame.display.flip()

        self.empty = self.time % cycle_time > cycle_time - empty_time

        for pos in visited:
            if not self.board.legal_pos(pos):
                print(f'Survived for {self.time} turns')
                self.ended = True
                return

        if not self.empty:
            self.board.update_occupancy(visited)
        else:
            self.board.update_occupancy()

    def has_ended(self) -> bool:
        return self.ended

    def end(self) -> None:
        self.ended = True
