import math


class Node:
    def __init__(self, name, cords=None):
        self.name = name
        if cords is None:
            cords = (0, 0)
        self.x, self.y = cords

    def __add__(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return 'name: {}, x: {}, y: {}'.format(self.name, self.x, self.y)


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

        self.weight = source + target

    def __repr__(self):
        return '{} - {}, weight: {}'.format(self.source.name, self.target.name, self.weight)


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        if not self.has_node(node):
            self.nodes.append(node)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_edge(self, edge):
        if self.is_possible_edge(edge):
            self.edges.append(edge)

    def has_node(self, node):
        return node in self.nodes

    def is_possible_edge(self, edge):
        return self.has_node(edge.source) and self.has_node(edge.target)

    def __str__(self):
        nodes = 'Nodes:\n' + '\n'.join([str(node) for node in self.nodes])
        edges = '\nEdges:\n' + '\n'.join([str(edge) for edge in self.edges])
        return nodes + edges


if __name__ == '__main__':
    g = Graph()
    lublin = Node('Lublin')
    warsaw = Node('Warsaw', (10, 10))

    w_l_edge = Edge(warsaw, lublin)
    g.add_nodes([warsaw, lublin])
    g.add_edge(w_l_edge)

    print(g)
