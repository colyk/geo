from math import sqrt
from queue import PriorityQueue
from typing import Dict, List, Optional

from numba import jit

from ..graph import Graph, Node


@jit(fastmath=True)
def heuristic(s_lat, s_lon, e_lat, e_lon):
    return sqrt((s_lat - e_lat) * (s_lat - e_lat) + (s_lon - e_lon) * (s_lon - e_lon))


@jit(forceobj=True)
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
                priority = new_cost + heuristic(
                    end.lat, end.lon, next_node.lat, next_node.lon
                )
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
