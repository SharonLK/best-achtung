from typing import List, Optional

import numpy as np

from point import Point
from segment import Segment


class Board:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.cells = np.zeros((self.width, self.height))

        self.occupancy = {idx: [] for idx in range(10)}

    def update_occupancy(self, pos1: Optional[np.ndarray] = None, pos2: Optional[np.ndarray] = None) -> None:
        for pos in self.occupancy[0]:
            self.cells[int(pos[0]), int(pos[1])] = 1

        for idx in range(1, 10):
            self.occupancy[idx - 1] = self.occupancy[idx]
            self.occupancy[idx] = []

        if pos1 is not None:
            self.occupancy[9] = [pos1, pos2]

    def _border_collision(self, pos: Point) -> bool:
        if pos.x >= self.width or pos.x < 0:
            return True
        elif pos.y >= self.height or pos.y < 0:
            return True
        else:
            return False

    def _path_collision(self, prev_pos: Point, cur_pos: Point, segments: List[Segment]) -> bool:
        move_segment = Segment(prev_pos, cur_pos)

        for segment in segments:
            if segment.intersects(move_segment):
                print('Oi Vei')
                return True

        return False

    # def legal_pos(self, pos: np.ndarray) -> bool:
    #     return not self._border_collision(pos) and not self._path_collision(pos)

    def legal_move(self, prev, curr, segments: List[Segment]):
        return not self._border_collision(curr) and not self._path_collision(prev, curr, segments)
