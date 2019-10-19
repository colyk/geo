from django.test import TestCase

from .graph import Node, Edge, Graph
from .utils import create_graph_from_geo_data


class UtilsCase(TestCase):
    def setUp(self) -> None:
        self.data = [[0, 0], [1, 1], [2, 2], [3, 3]]

    def test_creating_graph_from_geo_data(self):
        g = create_graph_from_geo_data(self.data)
        self.assertEqual(len(g.nodes), 4)
        self.assertEqual(len(g.edges), 6)


class NodeCase(TestCase):
    def setUp(self) -> None:
        self.node1 = Node(1, (0, 0))
        self.node2 = Node(2, (0, 1))

    def test_adding_nodes_return_distance(self):
        distance = self.node1 + self.node2
        self.assertEqual(distance, 1)


class GraphCase(TestCase):
    def setUp(self) -> None:
        self.node1 = Node(1, (0, 1))
        self.node2 = Node(2, (0, 2))
        self.node3 = Node(3, (0, 3))

        self.edge1 = Edge(self.node1, self.node2)
        self.edge2 = Edge(self.node2, self.node3)
        self.edge3 = Edge(self.node1, self.node3)
        self.g = Graph()

    def test_nodes_should_be_unique(self):
        self.g.add_node(self.node1)
        self.g.add_nodes([self.node1, self.node1])
        self.assertEqual(len(self.g.nodes), 1)

        self.g.add_node(self.node2)
        self.g.add_nodes([self.node2, self.node2])
        self.assertEqual(len(self.g.nodes), 2)

    def test_edge_should_not_be_added_if_graph_has_not_edge_nodes(self):
        self.g.add_node(self.node1)
        self.g.add_edge(self.edge1)
        self.assertEqual(len(self.g.edges), 0)

        self.g.add_node(self.node2)
        self.g.add_edge(self.edge1)
        self.assertEqual(len(self.g.edges), 1)

    def test_edges_should_be_unique(self):
        self.g.add_nodes([self.node1, self.node2])
        self.g.add_edge(self.edge1)
        self.g.add_edges([self.edge1, self.edge1])
        self.assertEqual(len(self.g.edges), 1)

    def test_edges_are_undirected(self):
        self.g.add_nodes([self.node1, self.node2])
        edge1 = Edge(self.node1, self.node2)
        edge2 = Edge(self.node2, self.node1)
        self.g.add_edges([edge1, edge2, Edge(self.node1, self.node2)])
        self.assertEqual(len(self.g.edges), 1)

    def test_connected_nodes(self):
        self.g.add_nodes([self.node1, self.node2, self.node3])
        self.g.add_edges([self.edge1, self.edge2, self.edge3])

        c_nodes = self.g.get_connected_nodes(self.node1)
        self.assertEqual(len(c_nodes), 2)

        c_nodes = self.g.get_connected_nodes(self.node2)
        self.assertEqual(len(c_nodes), 2)

        c_nodes = self.g.get_connected_nodes(self.node3)
        self.assertEqual(len(c_nodes), 2)
