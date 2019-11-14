import numpy as np

from . import cpp_a_star


def fast_a_star(graph, start, end):
    matrix = graph.matrix
    weights = matrix.matrix
    weights += 1

    s = matrix.get_node_idx(start)
    e = matrix.get_node_idx(end)
    path = cpp_a_star.astar_path(weights, s, e, allow_diagonal=False)
    print(path)
    path = [matrix.get_node_by_idx(idx[0]) for idx in path]
    return path
