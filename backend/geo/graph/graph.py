import math
from typing import List, Tuple, Union


class Node:
    __slots__ = ["name", "x", "y"]

    def __init__(self, name: Union[str, int], cords: Tuple[float, float]):
        self.name = name
        self.x, self.y = cords

    def __add__(self, other):
        """https://janakiev.com/blog/gps-points-distance-python/"""

        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __eq__(self, other):
        return self.name == other.name and self.x == other.x and self.y == other.y

    def __repr__(self):
        return "name: {}, x: {}, y: {}".format(self.name, self.x, self.y)

    def __hash__(self):
        return id(self)


class Edge:
    __slots__ = ["edge", "weight"]

    def __init__(self, source, target):
        self.edge = frozenset([source, target])
        self.weight = source + target


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
            edge_d = edge.edge.difference({node})
            if len(edge_d) == 1:
                conn_nodes.append(list(edge_d)[0])
        return conn_nodes

    def json(self) -> dict:
        r = {}

        for node in self.nodes:
            r[node.name] = {}
            for edge in self.edges:
                edge_d = edge.edge.difference({node})
                if len(edge_d) == 1:
                    r[node.name][list(edge_d)[0].name] = edge.weight
        return r

    def __str__(self):
        nodes = "Nodes:\n" + "\n".join([str(node) for node in self.nodes])
        return nodes


if __name__ == "__main__":
    g = Graph()
    lublin = Node("Lublin", (0, 0))
    warsaw = Node("Warsaw", (10, 10))

    w_l_edge = Edge(warsaw, lublin)
    g.add_nodes([warsaw, lublin])
    g.add_edge(w_l_edge)

    print(g)
    print(g.json())
