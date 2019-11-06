from collections import namedtuple

Bbox = namedtuple("Bbox", ["min_lat", "min_lon", "max_lat", "max_lon"])
Coord = namedtuple("Coord", ["lat", "lon"])
