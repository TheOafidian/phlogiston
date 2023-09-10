import random
import itertools
import logging
from dataclasses import dataclass


@dataclass
class Coordinates:
    x: float = random.random()
    y: float = random.random()
    z: float = random.random()

    def __post_init__(self):

        limit_max = max([self.x, self.y, self.z])
        limit_min = min([self.x, self.y, self.z])

        def normalize(f):
            return (f - limit_min) / (limit_max - limit_min)

        if limit_max > 1 or limit_min < 0:
            self.x = normalize(self.x)
            self.y = normalize(self.y)
            self.z = normalize(self.z)
            logging.warning(
                "Coordinates normalized to fit in a 0-1 range. New values {},{},{}".format(
                    self.x, self.y, self.z
                )
            )


@dataclass
class Sphere:
    """A class to keep track of information on a sphere"""

    id_iter = itertools.count()
    list = []

    def __init__(
        self, name: str, description: str = None, coords: Coordinates = Coordinates()
    ):
        self.sphere_no = next(Sphere.id_iter)
        self.name = name
        self.description = description
        self.coords = coords
        self.list.append(self)

    def __repr__(self) -> str:
        return f"[{self.sphere_no}] {self.name} ({self.coords.x},{self.coords.y},{self.coords.z})"

    def remove(self):
        Sphere.list.remove(self)

    def get(name: str):
        return [i for i in Sphere.list if i.name == name][0]


# TODO: wrangle list of spheres into a network obj and represent in 2D/3D with plotly

# TODO: write tool for importing spheres from a csv/tsv/xlsx
