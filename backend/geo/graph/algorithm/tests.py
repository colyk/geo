from django.test import TestCase

from .dijkstra import dijsktra
from ..graph import Node, Edge, Graph


class DijkstraCase(TestCase):
    def test_dijkstra_algorithm(self):
        g = Graph()

        node1 = Node("A", (0, 0))
        node2 = Node("B", (0, 1))
        node3 = Node("C", (0, 2))
        g.add_nodes([node1, node2, node3])

        edge1 = Edge(node1, node2)
        edge2 = Edge(node2, node3)
        g.add_edges([edge1, edge2])

        path = dijsktra(g, node1, node3)

        self.assertEqual(len(path), 3)
        self.assertIs(path[0], node1)
        self.assertIs(path[1], node2)
        self.assertIs(path[2], node3)

    def test_dijkstra_algorithm_without_solution(self):
        g = Graph()

        node1 = Node("A", (0, 0))
        node2 = Node("B", (0, 1))
        node3 = Node("C", (0, 2))
        g.add_nodes([node1, node2, node3])

        edge1 = Edge(node1, node2)
        g.add_edge(edge1)

        path = dijsktra(g, node1, node3)
        self.assertIsNone(path)
