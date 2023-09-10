import numpy as np
from phlogiston.io import read_spheres
from phlogiston.datatypes import Sphere, Coordinates

test_path = "tests/data/example-planes.csv"


def list_spheres(filename: str):

    df = read_spheres(filename)

    for i, sp in df.iterrows():
        coordinates = {}
        for co in ["x", "y", "z"]:
            if not np.isnan(sp[co]):
                coordinates[co] = sp[co]

        Sphere(sp.sphere, sp.desc, coords=Coordinates(**coordinates))

    return Sphere.list


def create_matrix(sphere_list, n=2):

    if n > 3 or n < 2:
        raise ValueError("Only 2 and 3 dimensional matrices are supported.")

    matrix_list = []
    for sphere in sphere_list:
        slice = [sphere.coords.x, sphere.coords.y]
        if n == 3:
            slice.append(sphere.coords.z)
        matrix_list.append(slice)

    return np.matrix(matrix_list)
