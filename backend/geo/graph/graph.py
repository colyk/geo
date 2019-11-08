from __future__ import annotations

import math
from decimal import Decimal, getcontext
from pprint import pprint
from typing import List, Tuple, Union, Dict, Any, Set, Callable

import numpy as np

"""
    Todo:
    Draw graph function
    Graph to adjacency matrix
"""
getcontext().prec = 10


class AdjacencyMatrix:
    __slots__ = ["matrix", "nodes"]

    def __init__(self, graph: Graph):
        self.nodes = list(sorted(graph.nodes, key=lambda n: n.name))
        nodes_count = len(self.nodes)
        self.matrix = np.zeros(nodes_count * nodes_count).reshape(
            (nodes_count, nodes_count)
        )

        for edge in graph.edges:
            n1, n2 = edge.edge
            idx1 = self.nodes.index(n1)
            idx2 = self.nodes.index(n2)
            self.matrix[idx1][idx2] = edge.weight
            self.matrix[idx2][idx1] = edge.weight


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

    def __eq__(self, other):
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

    def __eq__(self, other):
        return self.edge == other.edge

    def __repr__(self):
        f_node, s_node = self.edge
        return "{} {} - weight: {:.6f}".format(f_node, s_node, self.weight)

    def __hash__(self):
        return hash(repr(self))


class Graph:
    __slots__ = ["nodes", "edges"]

    def __init__(self, nodes: Set[Node] = None, edges: Set[Edge] = None):
        self.nodes: Set[Node] = nodes or set()
        self.edges: Set[Edge] = edges or set()

    def add_node(self, node: Node):
        if not self.has_node(node):
            self.nodes.add(node)

    def add_nodes(self, nodes: List[Node]) -> Graph:
        for node in nodes:
            self.add_node(node)
        return self

    def add_edge(self, edge: Edge):
        if self.is_possible_edge(edge) and not self.has_edge(edge):
            self.edges.add(edge)

    def add_edges(self, edges: Union[Set[Edge], List[Edge]]) -> Graph:
        for edge in edges:
            self.add_edge(edge)
        return self

    def has_node(self, node: Node) -> bool:
        return any(filter(lambda n: n == node, self.nodes))

    def is_possible_edge(self, edge: Edge) -> bool:
        return edge.edge.issubset(self.nodes)

    def has_edge(self, edge: Edge) -> bool:
        return any(filter(lambda e: e.edge == edge.edge, self.edges))  # type: ignore

    def get_connected_nodes(self, node: Node) -> List[Node]:
        conn_nodes = []
        for edge in self.edges:
            edge_difference = edge.edge - {node}
            if len(edge_difference) == 1:
                conn_node, = edge_difference
                conn_nodes.append(conn_node)
        return conn_nodes

    def get_node_edges(self, node: Node) -> List[Edge]:
        edges = []
        for edge in self.edges:
            edge_difference = edge.edge - {node}
            if len(edge_difference) == 1:
                edges.append(edge)
        return edges

    def json(self) -> Dict[Any, Dict]:
        json: Dict[Any, Dict] = {}

        for node in self.nodes:
            json[node.name] = {}
            for edge in self.edges:
                edge_difference = edge.edge - {node}
                if len(edge_difference) == 1:
                    conn_node, = edge_difference
                    json[node.name][conn_node.name] = edge.weight
        return json

    @property
    def matrix(self) -> AdjacencyMatrix:
        return AdjacencyMatrix(self)

    def __add__(self, other):
        nodes = self.nodes | other.nodes
        edges = self.edges | other.edges
        return Graph(nodes, edges)

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

    m = g.matrix
    print(m.matrix)
