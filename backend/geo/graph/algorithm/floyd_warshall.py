from math import inf
from itertools import product
from ..graph import Graph, Node, Edge


def floyd_warshall(graph: Graph):
    n = len(graph.nodes)
    rn = range(n)
    dist = [[inf] * n for _ in rn]
    nxt = [[0] * n for _ in rn]
    for i in rn:
        dist[i][i] = 0
    for u, v, w in graph.edges:
        dist[u - 1][v - 1] = w
        nxt[u - 1][v - 1] = v - 1
    for k, i, j in product(rn, repeat=3):
        sum_ik_kj = dist[i][k] + dist[k][j]
        if dist[i][j] > sum_ik_kj:
            dist[i][j] = sum_ik_kj
            nxt[i][j] = nxt[i][k]
    print("pair     dist    path")
    path = []
    for i, j in product(rn, repeat=2):
        if i != j:
            path = [i]
            while path[-1] != j:
                path.append(nxt[path[-1]][j])
            print(
                "%d → %d  %4d       %s"
                % (i + 1, j + 1, dist[i][j], " → ".join(str(p + 1) for p in path))
            )
    return path


if __name__ == "__main__":
    g = Graph()

    node1 = Node("A", (0, 0))
    node2 = Node("B", (0, 1))
    node3 = Node("C", (0, 2))
    g.add_nodes([node1, node2, node3])

    edge1 = Edge(node1, node2)
    edge2 = Edge(node2, node3)
    g.add_edges([edge1, edge2])

    r = floyd_warshall(g)

    print(r)
