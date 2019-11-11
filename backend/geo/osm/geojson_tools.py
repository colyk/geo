from itertools import combinations
from typing import Dict

from numba import jit

from ..graph.graph import Node, Graph, Edge
from ..osm import Coord


@jit(forceobj=True, parallel=True)
def create_graph_from_geojson(geojson: Dict) -> Graph:
    g = Graph()
    for feature in geojson["features"]:
        meta = feature["properties"]
        name = feature["id"]
        coords = feature["geometry"]["coordinates"]
        if feature["geometry"]["type"] == "Point":
            # Mainly it is a meta information
            continue

        prev_node = None
        for coord in coords:
            c = Coord(lon=coord[0], lat=coord[1])
            n = Node(name, c, meta)
            if prev_node is not None and n == prev_node:
                continue
            g.add_node(n)
            if prev_node is not None:
                g.add_edge(Edge(n, prev_node))
            prev_node = n

    # find interception nodes and connect them
    edges_combinations = combinations(g.edges, 2)
    for f_edge, s_edge in edges_combinations:
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

    return g


def cmp_node(f_node, s_node):
    return (
        f_node.lon == s_node.lon
        and f_node.lat == s_node.lat
        and f_node.name != s_node.name
    )
