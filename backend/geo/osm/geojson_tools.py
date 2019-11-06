from itertools import combinations
from pprint import pprint
from typing import Dict

import geojson

from ..graph.algorithm.dijkstra import dijkstra
from ..graph.graph import Node, Graph, Edge


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
            n = Node(name, coord, meta)
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

        if cmp_node(n1, n4):
            g.add_edge(Edge(n1, n4))

        if cmp_node(n2, n3):
            g.add_edge(Edge(n2, n3))

        if cmp_node(n2, n4):
            g.add_edge(Edge(n2, n4))

    return g


def cmp_node(f_node, s_node):
    return f_node.x == s_node.x and f_node.y == s_node.y and f_node.name != s_node.name


if __name__ == "__main__":
    # TODO: Make id of node unique. Add to node osm_id serial number of coord
    with open("export.geojson", "r", encoding="utf-8") as f:
        content = f.read()
        geojson = geojson.loads(content)
        graph = create_graph_from_geojson(geojson)
        print(graph)
        f_node, *_, l_node = tuple(sorted(graph.nodes, key=lambda n: n.name))
        path = dijkstra(graph, f_node, l_node)
        print("Shortest path: ")
        pprint(path)
