from __future__ import annotations
import numpy as np

import math
from decimal import Decimal, getcontext
from pprint import pprint
from typing import List, Tuple, Union, Dict, Any

"""
    Todo:
    Draw graph function
    Graph to adjacency matrix
"""
getcontext().prec = 10


class AdjacencyMatrix:
    __slots__ = ['matrix', 'nodes']

    def __init__(self, graph: Graph):
        sorted_nodes = sorted(graph.nodes, key=lambda n: n.name)
        nodes_count = len(graph.nodes)
        self.nodes = map(lambda n: n.name, sorted_nodes)
        self.matrix = np.zeros(nodes_count * nodes_count).reshape((nodes_count, nodes_count))


class Node:
    __slots__ = ["name", "meta", "x", "y"]

    def __init__(
        self,
        name: Union[str, int],
        cords: Tuple[float, float],
        meta: Union[Dict, None] = None,
    ):
        self.meta = meta
        self.name = name
        x, y = cords
        self.x = Decimal(x)
        self.y = Decimal(y)

    def __add__(self, other: Node):
        """https://janakiev.com/blog/gps-points-distance-python/"""

        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __eq__(self, other: Node):
        return self.name == other.name and self.x == other.x and self.y == other.y

    def __repr__(self):
        return "name: {}, x: {:.6f}, y: {:.6f}".format(self.name, self.x, self.y)

    def __hash__(self):
        return hash(repr(self))


class Edge:
    __slots__ = ["edge", "weight"]

    def __init__(self, f_node: Node, s_node: Node):
        self.edge = frozenset([f_node, s_node])
        self.weight = Decimal(f_node + s_node)

    def __eq__(self, other: Edge):
        return self.edge == other.edge

    def __repr__(self):
        f_node, s_node = self.edge
        return "{} {} - weight: {:.6f}".format(f_node, s_node, self.weight)

    def __hash__(self):
        return hash(repr(self))


class Graph:
    __slots__ = ["nodes", "edges"]

    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node: Node):
        if not self.has_node(node):
            self.nodes.add(node)

    def add_nodes(self, nodes: List[Node]):
        for node in nodes:
            self.add_node(node)

    def add_edge(self, edge: Edge):
        if self.is_possible_edge(edge) and not self.has_edge(edge):
            self.edges.add(edge)

    def add_edges(self, edges: List[Edge]):
        for edge in edges:
            self.add_edge(edge)

    def has_node(self, node: Node) -> bool:
        return any(filter(lambda n: n == node, self.nodes))

    def is_possible_edge(self, edge: Edge) -> bool:
        return edge.edge.issubset(self.nodes)

    def has_edge(self, edge: Edge) -> bool:
        return any(filter(lambda e: e.edge == edge.edge, self.edges))

    def get_connected_nodes(self, node: Node) -> List[Node]:
        conn_nodes = []
        for edge in self.edges:
            edge_difference = edge.edge - {node}
            if len(edge_difference) == 1:
                conn_node, = edge_difference
                conn_nodes.append(conn_node)
        return conn_nodes

    def json(self) -> Dict[Any, Dict]:
        json = {}

        for node in self.nodes:
            json[node.name] = {}
            for edge in self.edges:
                edge_difference = edge.edge - {node}
                if len(edge_difference) == 1:
                    conn_node, = edge_difference
                    json[node.name][conn_node.name] = edge.weight
        return json

    def matrix(self) ->AdjacencyMatrix:
        return AdjacencyMatrix(self)

    def __repr__(self):
        nodes = "Nodes:\n" + "\n".join([str(node) for node in self.nodes])
        edges = "\nEdges:\n" + "\n".join([str(edge) for edge in self.edges])
        return nodes + edges



if __name__ == "__main__":
    g = Graph()
    lublin = Node("Lublin", (0, 0))
    warsaw = Node("Warsaw", (10, 10))

    w_l_edge = Edge(warsaw, lublin)
    g.add_nodes([warsaw, lublin])
    g.add_edge(w_l_edge)

    print(g)
    pprint(g.json())

    m = g.matrix()
    print(m.matrix)
