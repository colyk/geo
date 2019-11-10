from typing import List


def build_path(graph):
    routes: List = []

    def find_paths(node, cities, path, distance):
        # Add way point
        path.append(node)

        # Calculate path length from current to last node
        if len(path) > 1:
            distance += cities[path[-2]][node]

        # If path contains all cities and is not a dead end,
        # add path from last to first city and return.
        if (len(cities) == len(path)) and (path[0] in cities[path[-1]].keys()):
            path.append(path[0])
            distance += cities[path[-2]][path[0]]
            routes.append([distance, path])
            return

        # Fork paths for all possible cities not yet used
        for city in cities:
            if (city not in path) and (node in cities[city].keys()):
                find_paths(city, dict(cities), list(path), distance)

    find_paths(0, graph, [], 0)
    return routes.sort()[0]
