from pprint import pprint
from typing import Union, List

from backend.geo.graph.graph import Graph, Node, Edge


def prim(graph: Graph):
    g = Graph()

    for node in graph.nodes:
        edges = graph.get_node_edges(node)
        min_weighted_edge = min(edges, key=lambda e: e.weight)
        g.add_node(node)
        g.add_edge(min_weighted_edge, force=True)
    return g


if __name__ == "__main__":
    g = Graph()

    node1 = Node("A", (0, 0))
    node2 = Node("B", (0, 1))
    node3 = Node("C", (0, 2))
    g.add_nodes([node1, node2, node3])

    edge1 = Edge(node1, node2)
    edge2 = Edge(node2, node3)
    edge3 = Edge(node1, node3)
    g.add_edges([edge1, edge2, edge3])

    r = prim(g)

    pprint(g)
    pprint(r)
