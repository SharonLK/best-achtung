from typing import List, Optional

import numpy as np
import pygame

from action import Action
from board import Board
from head import Head

speed = 20
dtheta = 0.3

radius = 5
path_radius = 5

cycle_time = 1500
empty_time = 150

screen_size = (800, 800)

p1_color = (255, 255, 255)
p2_color = (0, 255, 255)
p1_path_color = (255, 255, 0)
p2_path_color = (255, 0, 255)

BLACK = (0, 0, 0)


def as_int(pos: np.ndarray) -> List[int]:
    return [int(pos[0]), int(pos[1])]


# def draw_player(color, center, surface):
#     pygame.draw.circle(surface, color, center, radius)


# def draw_path(path, screen, color):
#     for point in path:
#         pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], path_radius)


class Game:
    def __init__(self):

        self.board: Optional[Board] = None
        self.head1: Optional[Head] = None
        self.head2: Optional[Head] = None
        self.winner: Optional[int] = None
        self.screen: Optional = None
        self.empty: Optional[bool] = False
        self.time = 0

        self.surface = np.full(screen_size, 0, dtype=np.int8)

        self.reset()

        self.ended = False

    @property
    def width(self):
        return screen_size[0]

    @property
    def height(self):
        return screen_size[1]

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

    def get_surface(self):
        return self.surface

    def reset(self) -> None:

        self.time = 0

        self.board = Board()
        self.surface = np.full(screen_size, 0, dtype=np.int8)

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
        self.winner = None
        self.empty = False

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)

    @staticmethod
    def _move_head(head: Head, action: Action) -> None:
        if action == Action.Right:
            head.change_direction(-dtheta)
        elif action == Action.Left:
            head.change_direction(dtheta)

        head.step()

    def _draw_player(self, color: float, position: np.ndarray) -> None:
        if position[0] < 0 or position[0] > screen_size[0] or position[1] < 0 or position[1] > screen_size[1]:
            return

        x = int(position[0])
        y = int(position[1])
        self.surface[x - 9:x + 9, y - 9:y + 9] = color

        # self.surface[int(position[0]), int(position[1])] = 1

    def advance(self, action1: Action, action2: Action) -> None:
        self.time += 1

        if self.empty:
            self._draw_player(0, self.head1.pos)
            self._draw_player(0, self.head2.pos)
        else:
            self._draw_player(1, self.head1.pos)
            self._draw_player(2, self.head2.pos)

        self._move_head(self.head1, action1)
        self._move_head(self.head2, action2)

        self._draw_player(1, self.head1.pos)
        self._draw_player(2, self.head2.pos)

        image = np.zeros((screen_size[0], screen_size[1], 3))
        image[self.surface == 1, :] = (255, 255, 255)
        image[self.surface == 2, :] = (0, 0, 0)

        self.screen.blit(pygame.surfarray.make_surface(image), (0, 0))
        # self.screen.blit(pygame.surfarray.make_surface(np.ones(screen_size, dtype=np.int8)), (0, 0))
        pygame.display.update()

        self.empty = self.time % cycle_time > cycle_time - empty_time

        if not self.board.legal_pos(self.head1.pos):
            # print('Player 1 has lost')
            self.ended = True
            self.winner = 2
            return

        # if not self.board.legal_pos(self.head2.pos):
        #     # print('Player 2 has lost')
        #     self.ended = True
        #     self.winner = 1
        #     return

        if not self.empty:
            self.board.update_occupancy(self.head1.pos, self.head2.pos)
        else:
            self.board.update_occupancy()

    def has_ended(self) -> bool:
        return self.ended

    def end(self) -> None:
        self.ended = True
