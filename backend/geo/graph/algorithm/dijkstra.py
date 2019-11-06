from pprint import pprint
from typing import Union, List, Dict, Tuple

from ..graph import Graph, Node, Edge


def dijkstra(graph: Graph, initial: Node, end: Node) -> Union[List[Node], None]:
    shortest_paths: Dict[Node, Tuple] = {initial: (None, 0)}
    current_node = initial
    visited_nodes = set()

    while current_node != end:
        visited_nodes.add(current_node)
        destinations = graph.get_connected_nodes(current_node)
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            # TODO: get current_node + next_node from edge
            weight = current_node + next_node + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {
            node: shortest_paths[node]
            for node in shortest_paths
            if node not in visited_nodes
        }
        if not next_destinations:
            return None
        current_node = min(next_destinations, key=lambda n: next_destinations[n][1])

    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    return path[::-1]


if __name__ == "__main__":
    g = Graph()

    node1 = Node("A", (0, 0))
    node2 = Node("B", (0, 1))
    node3 = Node("C", (0, 2))
    g.add_nodes([node1, node2, node3])

    edge1 = Edge(node1, node2)
    edge2 = Edge(node2, node3)
    g.add_edges([edge1, edge2])

    r = dijkstra(g, node1, node3)

    pprint(r)
