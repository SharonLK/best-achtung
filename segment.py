from dataclasses import dataclass

from point import Point


def ccw(a: Point, b: Point, c: Point):
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


# Return true if line segments AB and CD intersect
def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


@dataclass
class Segment:
    p1: Point
    p2: Point

    def intersects(self, other: 'Segment') -> bool:
        return intersect(self.p1, self.p2, other.p1, other.p2)
