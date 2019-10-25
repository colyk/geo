from pprint import pprint

from ..graph import Graph, Node, Edge


def prim(graph: Graph) -> Graph:
    g_ = Graph()
    nodes_ = []
    edges_ = set()

    for node in graph.nodes:
        node_edges = graph.get_node_edges(node)
        min_weighted_edge = min(node_edges, key=lambda e: e.weight)
        nodes_.append(node)
        edges_.add(min_weighted_edge)

    return g_.add_nodes(nodes_).add_edges(edges_)


if __name__ == "__main__":
    g = Graph()

    node1 = Node("A", (0, 0))
    node2 = Node("B", (3, 3))
    node3 = Node("C", (6, 0))
    node4 = Node("D", (3, 1.5))
    g.add_nodes([node1, node2, node3, node4])

    edges = [
        Edge(node1, node2),
        Edge(node2, node3),
        Edge(node3, node4),
        Edge(node1, node3),
        Edge(node1, node4),
        Edge(node2, node4),
    ]
    g.add_edges(edges)

    r = prim(g)

    pprint(g)
    pprint(r)
