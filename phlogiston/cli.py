import argparse
import importlib.util
from phlogiston.io import return_outputname, log
from phlogiston.plot import plot_graph, make_printer_friendly
import phlogiston.handlers as ph

test_path = "tests/data/example-planes.csv"

AVAILABLE_COMMANDS = ["chart", "random"]
EXTENSIONS_OUT = ["html", "pdf", "png"]
SHEET_LONG = 3508
SHEET_SHORT = 2480


def main(args=None):

    # COMMAND PARSER ################
    parser = argparse.ArgumentParser(
        prog="phlogiston",
        description="Fantasy Starchart mapper",
    )
    subparsers = parser.add_subparsers(help="commands", required=True)

    # CHART PARSER ##################

    def extension(string: str):
        return string.strip(".")

    chart_parser = subparsers.add_parser(
        AVAILABLE_COMMANDS[0], help="Chart a starmap from an existing input file."
    )
    chart_parser.add_argument("filename")
    chart_parser.add_argument("--output", "-o", default="/", help="Name of file to save output map to.")
    chart_parser.add_argument(
        "--extension", "-e", type=extension, choices=EXTENSIONS_OUT, default="html", help= "Extension to save output as."
    )
    chart_parser.add_argument("--dimensions", "-n", default=2, type=int, choices=[2,3], help="Amount of dimensions to plot.")
    chart_parser.add_argument("--radius", "-r", default=0.2, type=float, help="Relative distance two spheres can maximally have to draw routes between them (0-1).")
    chart_parser.add_argument("--distance_metric", "-p", default=2, type=float, help="Minkowski distance metric to use.")
    chart_parser.add_argument("--name", "-s", default="", type=str, help="Name of the starchart. Gets added to the top of the figure.")
    chart_parser.add_argument("--dtime", "-t", default=1, type=float, help="Modifier to the distance in time betweeen different spheres.")
    chart_parser.set_defaults(func=chart_from_file)

    # RANDOM PARSER #################

    random_parser = subparsers.add_parser(
        AVAILABLE_COMMANDS[1],
        help="Generate random coordinates for a starchart and save to a file.",
    )
    random_parser.add_argument("filename")
    random_parser.set_defaults(func=generate_random_chart)

    #################################
    
    args = parser.parse_args(args)
    args.func(args)


def chart_from_file(args):
    foutname = return_outputname(args.filename, args.output, args.extension)
    ls = ph.list_spheres(args.filename)
    sphere_n = {l.sphere_no: l.name for l in ls}
    net = ph.create_network(ls, args.dimensions, args.radius, args.distance_metric)
    fig = plot_graph(net, sphere_n, map_name=args.name, distance_corr=args.dtime)

    if args.extension == "html":
        fig.write_html(foutname)
        return foutname

    if args.extension == "pdf":
        # write garbage graph, to get rid of loading bar bug in kaleido
        import plotly.express as px
        import time

        gfig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
        gfig.write_image(foutname, format="pdf")
        time.sleep(2)

        make_printer_friendly(fig).write_image(
            foutname, format="pdf", width=SHEET_LONG, height=SHEET_SHORT, scale=2
        )
    elif args.extension == "png":
        fig.write_image(foutname, format="png")
    return foutname


def generate_random_chart(args):
    pass


if __name__ == "__main__":
    main()
