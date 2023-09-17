import numpy as np
import networkx as nx
from phlogiston.datatypes import Sphere, Coordinates
from phlogiston.io import read_spheres

def list_spheres(filename: str):

    df = read_spheres(filename)
    Sphere.list = []

    for i, sp in df.iterrows():
        coordinates = {}
        for co in ["x", "y", "z"]:
            if not np.isnan(sp[co]):
                coordinates[co] = sp[co]

        Sphere(sp.sphere, sp.desc, coords=Coordinates(**coordinates))

    return Sphere.list


def _get_pos_dict(sphere_list, n=2):

    if n > 3 or n < 2:
        raise ValueError("Only 2 and 3 dimensional matrices are supported.")

    positions = {}
    for sphere in sphere_list:
        slice = [sphere.coords.x, sphere.coords.y]
        if n == 3:
            slice.append(sphere.coords.z)
        positions[sphere.sphere_no] = slice

    return positions


def create_network(sphere_list, n=2, radius=0.2, p=0.1):
    """
    sphere_list: list of Sphere objects
    n:  dimensions to use
    radius: max distance to be considered 'adjacent'
    p : float, optional
        Which Minkowski distance metric to use.  `p` has to meet the condition
        ``1 <= p <= infinity``.
    """
    pos = _get_pos_dict(sphere_list, n)
    network = nx.empty_graph([s.sphere_no for s in sphere_list])
    nx.set_node_attributes(network, pos, "pos")
    network.add_edges_from(nx.geometric_edges(network, radius, p))

    return network
