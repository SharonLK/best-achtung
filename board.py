from typing import Optional

import numpy as np


class Board:

    def __init__(self, width: int = 1200, height: int = 900):
        self.width = width
        self.height = height
        self.cells = np.zeros((self.width, self.height))

        self.occupancy = {idx: [] for idx in range(10)}

    def update_occupancy(self, pos1: Optional[np.ndarray] = None, pos2: Optional[np.ndarray] = None) -> None:
        for pos in self.occupancy[0]:
            self.cells[int(pos[0]), int(pos[1])] = 1

        for idx in range(1, 10):
            self.occupancy[idx-1] = self.occupancy[idx]
            self.occupancy[idx] = []

        if pos1 is not None:
            self.occupancy[9] = [pos1, pos2]

    def _border_collision(self, pos: np.ndarray) -> bool:
        if pos[0] >= self.width or pos[0] < 0:
            return True
        elif pos[1] >= self.height or pos[1] < 0:
            return True
        else:
            return False

    def _path_collision(self, pos: np.ndarray) -> bool:
        return self.cells[int(pos[0]), int(pos[1])] == 1

    def legal_pos(self, pos: np.ndarray) -> bool:
        return not self._border_collision(pos) and not self._path_collision(pos)
