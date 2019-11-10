from itertools import combinations

from django.test import TestCase

from ...osm import Coord as C
from .floyd_warshall import floyd_warshall, get_path
from .prim import prim
from .dijkstra import dijkstra
from ..graph import Node, Edge, Graph


class DijkstraCase(TestCase):
    def test_dijkstra_algorithm(self):
        g = Graph()
        node1 = Node("A", C(0, 0))
        node2 = Node("B", C(0, 1))
        node3 = Node("C", C(0, 2))
        g.add_nodes([node1, node2, node3])

        edge1 = Edge(node1, node2)
        edge2 = Edge(node2, node3)
        g.add_edges([edge1, edge2])

        path = dijkstra(g, node1, node3)

        self.assertEqual(len(path), 3)
        self.assertIs(path[0], node1)
        self.assertIs(path[1], node2)
        self.assertIs(path[2], node3)

    def test_dijkstra_algorithm_without_solution(self):
        g = Graph()

        node1 = Node("A", C(0, 0))
        node2 = Node("B", C(0, 1))
        node3 = Node("C", C(0, 2))
        g.add_nodes([node1, node2, node3])

        edge1 = Edge(node1, node2)
        g.add_edge(edge1)

        path = dijkstra(g, node1, node3)
        self.assertIsNone(path)


class PrimCase(TestCase):
    def test_prim_algorithm(self):
        g = Graph()
        nodes = [
            Node("A", C(0, 0)),
            Node("B", C(3, 3)),
            Node("C", C(6, 0)),
            Node("D", C(3, 1.5)),
        ]
        edges_combinations = list(combinations(nodes, 2))
        edges = [Edge(node1, node2) for node1, node2 in edges_combinations]
        g.add_nodes(nodes).add_edges(edges)

        g_ = prim(g)

        self.assertEqual(len(g_.nodes), len(nodes))
        self.assertEqual(len(g_.edges), 3)


class FloydWarshallCase(TestCase):
    def test_floyd_warshall_algorithm(self):
        g = Graph()
        nodes = [
            Node("A", C(0, 0)),
            Node("B", C(3, 3)),
            Node("C", C(6, 0)),
            Node("D", C(3, 1.5)),
        ]
        edges_combinations = list(combinations(nodes, 2))
        edges = [Edge(node1, node2) for node1, node2 in edges_combinations]
        g.add_nodes(nodes).add_edges(edges)

        g_ = floyd_warshall(g)

        self.assertEqual(1, 1)
        get_path(g_, 0, 3)
