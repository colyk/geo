import math
from queue import PriorityQueue
from typing import Dict, List, Optional

from ..graph import Graph, Node


def heuristic(start: Node, end: Node):
    s_lat = start.lat
    s_lon = start.lon
    e_lat = end.lat
    e_lon = end.lon
    return math.sqrt((s_lat - e_lat) ** 2 + (s_lon - e_lon) ** 2)


def a_star(graph: Graph, start: Node, end: Node) -> Optional[List[Node]]:
    current_node = None

    frontier: PriorityQueue = PriorityQueue()
    frontier.put((0, start))

    shortest_paths: Dict[Node, Optional[Node]] = {start: None}
    costs: Dict[Node, float] = {start: 0}

    while not frontier.empty():
        _, current_node = frontier.get()
        if current_node == end:
            break

        for next_node in graph.get_connected_nodes(current_node):
            new_cost = (current_node + next_node) + costs[current_node]
            if next_node not in costs or new_cost < costs[next_node]:
                costs[next_node] = new_cost
                priority = new_cost + heuristic(end, next_node)
                frontier.put((priority, next_node))
                shortest_paths[next_node] = current_node

    path = []
    while current_node is not None:
        path.append(current_node)
        n_node: Optional[Node] = shortest_paths[current_node]
        current_node = n_node

    path.reverse()
    if path[-1] != end:
        return None

    return path
