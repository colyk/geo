from typing import Union, List, Dict, Tuple

from ..graph import Graph, Node


def dijkstra(graph: Graph, start: Node, end: Node) -> Union[List[Node], None]:
    shortest_paths: Dict[Node, Tuple] = {start: (None, 0)}
    current_node = start
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
