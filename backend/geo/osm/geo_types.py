from collections import namedtuple


class Bbox(namedtuple("Bbox", ["min_lat", "min_lon", "max_lat", "max_lon"])):
    __slots__ = ()

    def __str__(self):
        return f"{self.min_lat},{self.min_lon},{self.max_lat},{self.max_lon}"


Coord = namedtuple("Coord", ["lat", "lon"])
