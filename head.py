from typing import List

import numpy as np

from point import Point
from segment import Segment


class Head:
    def __init__(self, pos: np.ndarray, direction: float, speed: float):
        self.trail: List[Segment] = []
        self.points: List[Point] = [Point(pos[1], pos[0])]
        self.pos = pos
        self.direction = direction
        self.speed = speed

        self.steps = 0

    @property
    def x(self):
        return self.pos[1]

    @property
    def y(self):
        return self.pos[0]

    def distance(self, other: 'Head'):
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def change_direction(self, change: float) -> None:
        self.direction += change

    def step(self) -> None:
        self.steps += 1

        prev_x = self.x
        prev_y = self.y
        new_x = self.x + self.speed * np.cos(self.direction)
        new_y = self.y + self.speed * np.sin(self.direction)

        self.pos = np.array([new_y, new_x])

        if (self.steps // 10) % 5 >= 4:
            return

        self.points.append(Point(self.x, self.y))
        self.trail.append(Segment(Point(prev_x, prev_y), Point(new_x, new_y)))
