from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def distance_squared(self, other: 'Point') -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
