from typing import List

import numpy as np


class Head:

    def __init__(self, pos: np.ndarray, direction: float, speed: int):
        self.pos = pos
        self.direction = direction
        self.speed = speed

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

    def step(self) -> List[np.ndarray]:

        visited = []
        for _ in range(self.speed):
            new_x = self.x + np.cos(self.direction)
            new_y = self.y + np.sin(self.direction)
            self.pos = np.array([new_y, new_x])
            visited.append(self.pos)

        return visited
