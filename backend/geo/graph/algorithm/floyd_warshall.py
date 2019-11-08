from itertools import product

import numpy as np

from ..graph import Graph, Node, Edge


def floyd_warshall(graph: Graph):
    matrix = graph.matrix
    m = matrix.matrix
    v = len(m)
    p = np.zeros(m.shape)
    for i in range(0, v):
        for j in range(0, v):
            p[i][j] = i
            if i != j and m[i][j] == 0:
                m[i][j] = float("inf")
                p[i][j] = float("-inf")

    for k in range(0, v):
        for i in range(0, v):
            for j in range(0, v):
                sum_ = m[i][k] + m[k][j]
                if m[i][j] > sum_:
                    m[i][j] = sum_
                    p[i][j] = p[k][j]
    return p


def get_path(p, i, j):
    path = []

    def find(p, i, j):
        if i == j:
            path.append(i)
        elif p[i][j] == float("-inf"):
            path.append(i)
            path.append(j)
        else:
            find(p, i, p[i][j])
            path.append(j)

    find(p, i, j)
    return path
