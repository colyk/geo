from .graph import Graph, Node, Edge


def create_graph_from_geo(data):
    points = data["points"]
    g = Graph()
    nodes = []
    edges = []

    for idx, point in enumerate(points):
        nodes.append(Node(idx, point))

    for i in range(0, len(nodes)):
        for j in range(0, len(nodes)):
            if i != j:
                edges.append(Edge(nodes[i], nodes[j]))

    g.add_nodes(nodes)
    g.add_edges(edges)

    return g
