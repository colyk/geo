from itertools import combinations
from typing import List

from .graph import Graph, Node, Edge


def create_graph_from_geo_data(points: List) -> Graph:
    g = Graph()

    for idx, point in enumerate(points):
        g.add_node(Node(idx, point))

    edges_combinations = list(combinations(g.nodes, 2))
    edges = [Edge(node1, node2) for node1, node2 in edges_combinations]
    g.add_edges(edges)

    return g
