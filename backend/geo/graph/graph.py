import math


def haversine(coord1, coord2):
    """https://janakiev.com/blog/gps-points-distance-python/"""
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class Node:
    def __init__(self, name, cords=None):
        self.name = name
        if cords is None:
            cords = (0, 0)
        self.x, self.y = cords

    def __add__(self, other):
        return haversine((self.x, self.y), (other.x, other.y))

    def __repr__(self):
        return "name: {}, x: {}, y: {}".format(self.name, self.x, self.y)


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

        self.weight = source + target

    def __repr__(self):
        return "{} - {}, weight: {}".format(
            self.source.name, self.target.name, self.weight
        )


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
        if self.is_possible_edge(edge) and edge not in self.edges:
            self.edges.append(edge)

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)

    def has_node(self, node):
        return node in self.nodes

    def is_possible_edge(self, edge):
        return self.has_node(edge.source) and self.has_node(edge.target)

    def json(self):
        r = {}

        for node in self.nodes:
            r[node.name] = {}
            for edge in self.edges:
                if edge.source.name == node.name:
                    r[node.name][edge.target.name] = edge.weight
                if edge.target.name == node.name:
                    r[node.name][edge.source.name] = edge.weight

        return r

    def __str__(self):
        nodes = "Nodes:\n" + "\n".join([str(node) for node in self.nodes])
        edges = "\nEdges:\n" + "\n".join([str(edge) for edge in self.edges])
        return nodes + edges


if __name__ == "__main__":
    g = Graph()
    lublin = Node("Lublin")
    warsaw = Node("Warsaw", (10, 10))

    w_l_edge = Edge(warsaw, lublin)
    g.add_nodes([warsaw, lublin])
    g.add_edge(w_l_edge)

    print(g)
