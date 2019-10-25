from ..graph import Graph


def prim(graph: Graph) -> Graph:
    spanning_tree = Graph()
    s_nodes = []
    s_edges = set()

    for node in graph.nodes:
        node_edges = graph.get_node_edges(node)
        min_weighted_edge = min(node_edges, key=lambda e: e.weight)
        s_nodes.append(node)
        s_edges.add(min_weighted_edge)

    return spanning_tree.add_nodes(s_nodes).add_edges(s_edges)
