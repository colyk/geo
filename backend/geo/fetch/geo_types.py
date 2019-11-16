from collections import namedtuple


class Bbox(namedtuple("Bbox", ["min_lat", "min_lon", "max_lat", "max_lon"])):
    __slots__ = ()

    def __str__(self):
        return f"{self.min_lat},{self.min_lon},{self.max_lat},{self.max_lon}"

    @classmethod
    def parse(cls, s_bbox):
        bbox = list(map(float, s_bbox.split(",")))
        return cls(min_lat=bbox[0], min_lon=bbox[1], max_lat=bbox[2], max_lon=bbox[3])


Coord = namedtuple("Coord", ["lat", "lon"])
