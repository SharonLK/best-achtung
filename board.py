from typing import Optional, List

import numpy as np

from head import Head


class Board:

    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.cells = np.zeros((self.width, self.height))

        self.occupancy = {idx: [] for idx in range(3)}

    def update_occupancy(self, pos_lst: List[np.ndarray] = None) -> None:
        for pos in self.occupancy[0]:
            self.cells[int(pos[0]), int(pos[1])] = 1

        for idx in range(1, 10):
            self.occupancy[idx-1] = self.occupancy[idx]
            self.occupancy[idx] = []

        if pos_lst is not None:
            self.occupancy[2] = pos_lst

    def _border_collision(self, pos: np.ndarray) -> bool:
        if pos[0] > self.width - 1 or pos[0] < 1:
            return True
        elif pos[1] > self.height - 1 or pos[1] < 1:
            return True
        else:
            return False

    def _path_collision(self, pos: np.ndarray) -> bool:
        collide = self.cells[int(pos[0]), int(pos[1])] \
                  or self.cells[int(pos[0]) - 1, int(pos[1])] \
                  or self.cells[int(pos[0]) + 1, int(pos[1])] \
                  or self.cells[int(pos[0]), int(pos[1]) + 1] \
                  or self.cells[int(pos[0]), int(pos[1]) - 1] \
                  or self.cells[int(pos[0]) - 1, int(pos[1]) - 1] \
                  or self.cells[int(pos[0]) + 1, int(pos[1]) + 1] \
                  or self.cells[int(pos[0]) - 1, int(pos[1]) + 1] \
                  or self.cells[int(pos[0]) + 1, int(pos[1]) - 1]
        return bool(collide)

    def legal_pos(self, pos: np.ndarray) -> bool:
        return not self._border_collision(pos) and not self._path_collision(pos)

    def risks(self, head: Head) -> np.ndarray:

        top_left = np.sum(self.cells[head.pos[0] - 30:head.pos[0], head.pos[1] - 30:head.pos[1]])
        top_right = np.sum(self.cells[head.pos[0] - 30:head.pos[0], head.pos[1]:head.pos[1] + 30])
        bottom_right = np.sum(self.cells[head.pos[0]:head.pos[0] + 30, head.pos[1]:head.pos[1] + 30])
        bottom_left = np.sum(self.cells[head.pos[0]:head.pos[0] + 30, head.pos[1] - 30:head.pos[1]])

        return np.array([top_left, top_right, bottom_right, bottom_left])
