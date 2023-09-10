import random
import itertools
from dataclasses import dataclass

@dataclass
class Coordinates:
    x: float = random.random()
    y: float = random.random()
    z: float = random.random()

@dataclass
class Plane():
    """A class to keep track of information on a plane"""
    id_iter = itertools.count()
    list = []

    def __init__(self, name:str, description:str=None, coords:Coordinates = Coordinates()):
        self.planet_no = next(Plane.id_iter)
        self.name = name
        self.description = description
        self.coords = coords
        self.list.append(self)
    
    def __repr__(self) -> str:
        return f"[{self.planet_no}] {self.name} ({self.coords.x},{self.coords.y},{self.coords.z})"

    def remove(self):
        Plane.list.remove(self)
    
    def get(name:str):
        return [i for i in Plane.list if i.name == name][0]

# TODO: wrangle list of planes into a network obj and represent in 2D/3D with plotly

# TODO: write tool for importing planes from a csv/tsv/xlsx
