"""
The Ramer-Douglas-Peucker algorithm http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
"""
from math import sqrt
from typing import List


def point_line_distance(point, start, end):
    n = abs(
        (end[0] - start[0]) * (start[1] - point[1])
        - (start[0] - point[0]) * (end[1] - start[1])
    )
    d = sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    return n / d


def rdp(points: List, epsilon: float) -> List[List[float]]:
    """
    Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = rdp(points[: index + 1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]

    return results


if __name__ == "__main__":
    d = [[0, 0], [1, 1], [1.1, 1.1], [2, 2]]
    rdp_d = rdp(d, 0.1)  # [[0, 0], [2, 2]]
    print(rdp_d)
