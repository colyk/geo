from itertools import combinations
from typing import Dict, List

from numba import jit

from ..fetch import Coord
from ..graph.graph import Node, Graph, Edge


def create_graph_from_geojson(geojson: Dict) -> Graph:
    g = Graph()
    for feature in geojson["features"]:
        # meta = feature["properties"]
        name = feature["id"]
        coords = feature["geometry"]["coordinates"]
        if feature["geometry"]["type"] == "Point":
            # Mainly it is a meta information
            continue
        try:
            connect_nodes(coords, g, name)
        except ValueError:
            print("Build graph data error")

    connect_intercepted_nodes(g)
    return g


@jit(forceobj=True)
def connect_nodes(coords: List, g: Graph, name: str) -> None:
    prev_node = None
    for coord in coords:
        c = Coord(lon=coord[0], lat=coord[1])
        n = Node(name, c)
        if prev_node is not None and cmp_node(n, prev_node):
            continue
        g.add_node(n)
        if prev_node is not None:
            g.add_edge(Edge(n, prev_node))
        prev_node = n


@jit(forceobj=True)
def connect_intercepted_nodes(g: Graph) -> None:
    for f_edge, s_edge in combinations(g.edges, 2):
        n1, n2 = f_edge.edge
        n3, n4 = s_edge.edge
        if cmp_node(n1, n3):
            g.add_edge(Edge(n1, n3))
        elif cmp_node(n1, n4):
            g.add_edge(Edge(n1, n4))
        elif cmp_node(n2, n3):
            g.add_edge(Edge(n2, n3))
        elif cmp_node(n2, n4):
            g.add_edge(Edge(n2, n4))


@jit(forceobj=True)
def cmp_node(f_node, s_node):
    return (
        f_node.lon == s_node.lon
        and f_node.lat == s_node.lat
        and f_node.name != s_node.name
    )
