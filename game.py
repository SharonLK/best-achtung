import math
import random
from typing import List, Optional

import numpy as np
import pygame

from action import Action
from board import Board
from head import Head
from point import Point
from segment import Segment

speed = 5
dtheta = 0.2

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

ITERATIONS_TO_OBSTACLE = 50


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

        self.obstacles: List[Segment] = []
        self.iterations = 0

        self.obstacles: List[Segment] = []
        self.obstacles_points: List[Point] = []
        self.iterations_to_obstacle = ITERATIONS_TO_OBSTACLE

        self.border_points = []
        for i in range(0, 800, 10):
            self.border_points.append(Point(0, i))
            self.border_points.append(Point(800, i))
            self.border_points.append(Point(i, 0))
            self.border_points.append(Point(i, 800))

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

        self.obstacles: List[Segment] = []
        self.obstacles_points: List[Point] = []
        self.iterations_to_obstacle = ITERATIONS_TO_OBSTACLE

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
        self.iterations_to_obstacle -= 1

        if self.iterations_to_obstacle <= 0:
            p1 = Point(random.randint(0, 800), random.randint(0, 800))
            while math.sqrt(p1.distance_squared(Point(self.head1.x, self.head1.y))) <= 250:
                p1 = Point(random.randint(0, 800), random.randint(0, 800))

            p2 = Point(p1.x + random.randint(-50, 50), p1.y + random.randint(-50, 50))
            p2 = Point(min(self.width, max(0, int(p2.x))), min(self.height, max(0, int(p2.y))))
            # while math.sqrt(p1.distance_squared(p2)) > 20:
            #     p2 = Point(random.randint(0, 800), random.randint(0, 800))

            self.obstacles.append(Segment(p1, p2))
            for i in range(8):
                self.obstacles_points.append(Point(
                    x=p1.x + ((p2.x - p1.x) / 7) * 8,
                    y=p1.y + ((p2.y - p1.y) / 7) * 8
                ))
                # self.obstacles_points += [p1, p2]

            self.iterations_to_obstacle = ITERATIONS_TO_OBSTACLE

        # if self.empty:
        #     self._draw_player(0, self.head1.pos)
        #     self._draw_player(0, self.head2.pos)
        # else:
        #     self._draw_player(1, self.head1.pos)
        # self._draw_player(2, self.head2.pos)

        prev1_pos = self.head1.pos

        self._move_head(self.head1, action1)
        self._move_head(self.head2, action2)

        self._draw_player(1, self.head1.pos)
        # self._draw_player(2, self.head2.pos)

        image = np.zeros((screen_size[0], screen_size[1], 3))
        image[self.surface == 1, :] = (255, 255, 255)

        # self.screen.blit(pygame.surfarray.make_surface(image), (0, 0))
        # self.screen.blit(pygame.surfarray.make_surface(np.ones(screen_size, dtype=np.int8)), (0, 0))

        self.screen.fill('black')

        for segment in self.head1.trail[:-1]:
            # pygame.draw.line(self.screen, 'white',
            #                  (prev1_pos[0], prev1_pos[1]),
            #                  (self.head1.pos[0], self.head1.pos[1]))
            pygame.draw.line(self.screen, 'white', (segment.p1.x, segment.p1.y), (segment.p2.x, segment.p2.y),
                             width=3)

        for segment in self.obstacles:
            pygame.draw.line(self.screen, 'orange', (segment.p1.x, segment.p1.y), (segment.p2.x, segment.p2.y),
                             width=3)

        # pygame.draw.line(self.screen, 'red',
        #                  (prev1_pos[1], prev1_pos[0]),
        #                  (self.head1.pos[1], self.head1.pos[0]))

        pygame.draw.circle(self.screen, 'red', (self.head1.x, self.head1.y), 5)

        # position = Point(self.head1.x, self.head1.y)
        # closest = 1131 ** 2
        # closest1 = 1131 ** 2
        # closest1_minus = 1131 ** 2
        # closest_point = None
        # closest_point1 = None
        # closest_point1_minus = None
        # for point in self.head1.points[:-10] + self.obstacles_points + self.border_points:
        #     direction_to_point = math.degrees(math.atan2(point.y - position.y, point.x - position.x)) % 360
        #     actual_direction = math.degrees(self.head1.direction) % 360
        #     delta_direction = (direction_to_point - actual_direction) % 360
        #     # print(self.game.head1.direction % (math.pi * 2), direction_to_point % (math.pi * 2))
        #     # print(actual_direction)
        #
        #     if delta_direction < 5 or delta_direction > 355:
        #         distance_squared = point.distance_squared(position)
        #         if distance_squared < closest:
        #             closest = distance_squared
        #             closest_point = point
        #
        #     if 5 <= delta_direction < 15:
        #         distance_squared = point.distance_squared(position)
        #         if distance_squared < closest1:
        #             closest1 = distance_squared
        #             closest_point1 = point
        #
        #     if 345 < delta_direction <= 355:
        #         distance_squared = point.distance_squared(position)
        #         if distance_squared < closest1_minus:
        #             closest1_minus = distance_squared
        #             closest_point1_minus = point
        #
        # if closest_point is not None:
        #     pygame.draw.circle(self.screen, 'green', (closest_point.x, closest_point.y), 5)
        # if closest_point1 is not None:
        #     pygame.draw.circle(self.screen, 'yellow', (closest_point1.x, closest_point1.y), 5)
        # if closest_point1_minus is not None:
        #     pygame.draw.circle(self.screen, 'blue', (closest_point1_minus.x, closest_point1_minus.y), 5)

        pygame.display.update()

        self.empty = self.time % cycle_time > cycle_time - empty_time

        if not self.board.legal_move(Point(prev1_pos[1], prev1_pos[0]),
                                     Point(self.head1.pos[1], self.head1.pos[0]),
                                     self.head1.trail[:-5] + self.obstacles):
            print(f'Player 1 has lost {len(self.head1.points)}')
            self.ended = True
            self.winner = 2
            return

        # if not self.board.legal_pos(self.head2.pos):
        #     # print('Player 2 has lost')
        #     self.ended = True
        #     self.winner = 1
        #     return

        # if not self.empty:
        #     self.board.update_occupancy(self.head1.pos, self.head2.pos)
        # else:
        #     self.board.update_occupancy()

    def has_ended(self) -> bool:
        return self.ended

    def end(self) -> None:
        self.ended = True
