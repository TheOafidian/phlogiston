import numpy as np
import networkx as nx
from phlogiston.io import read_spheres
from phlogiston.datatypes import Sphere, Coordinates
from phlogiston.plot import plot_graph

test_path = "tests/data/example-planes.csv"

AVAILABLE_COMMANDS = ["chart", "random"]


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
    for i, sphere in enumerate(sphere_list):
        slice = [sphere.coords.x, sphere.coords.y]
        if n == 3:
            slice.append(sphere.coords.z)
        positions[i] = slice

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
    network = nx.empty_graph(len(sphere_list))
    nx.set_node_attributes(network, pos, "pos")
    network.add_edges_from(nx.geometric_edges(network, radius, p))

    return network


def main():
    import argparse

    # COMMAND PARSER ################
    parser = argparse.ArgumentParser(
        prog="phlogiston",
        description="Fantasy Starchart mapper",
    )
    parser.add_argument("command", choices=AVAILABLE_COMMANDS)

    command_parsers = {}

    # CHART PARSER ##################
    chart_parser = argparse.ArgumentParser(
        prog=f"phlogiston {AVAILABLE_COMMANDS[0]}",
        description="Fantasy Starchart mapper from input file",
    )
    chart_parser.add_argument("filename")
    chart_parser.add_argument("--dimensions", "-n", default=2)
    chart_parser.add_argument("--radius", "-r", default=0.2)
    chart_parser.add_argument("--distance_metric", "-p", default=0.1)
    chart_parser.add_argument("--name", "-s", default="")
    chart_parser.add_argument("--dtime", "-t", default=1)

    
    command_parsers[AVAILABLE_COMMANDS[0]] = chart_parser

    # RANDOM PARSER #################

    random_parser = argparse.ArgumentParser(
        prog=f"phlogiston {AVAILABLE_COMMANDS[1]}",
        description="Generate random coordinates for a starchart",
    )
    random_parser.add_argument("filename")
    command_parsers[AVAILABLE_COMMANDS[1]] = random_parser
    #################################
    args, options = parser.parse_known_args()
    cargs = command_parsers[args.command].parse_args(options)

    if args.command == AVAILABLE_COMMANDS[0]:        
        chart_from_file(cargs.filename, 
                        cargs.dimensions, cargs.radius, cargs.distance_metric,
                        cargs.name, cargs.dtime)


def chart_from_file(filename, n, radius, p, name, dtime):
    ls = list_spheres(filename)
    sphere_n = {l.sphere_no:l.name for l in ls}
    net = create_network(ls, n, radius, p)
    fig = plot_graph(net, sphere_n, map_name=name, distance_corr=dtime)

    # TODO: write handler for output types
    fig.write_html("Test-starchart.html")


def generate_random_chart():
    pass


if __name__ == "__main__":
    main()
