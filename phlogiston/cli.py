import importlib.util
from phlogiston.io import return_outputname, log
from phlogiston.plot import plot_graph, make_printer_friendly
import phlogiston.handlers as ph

test_path = "tests/data/example-planes.csv"

AVAILABLE_COMMANDS = ["chart", "random"]
EXTENSIONS_OUT = ["html", "pdf", "png"]
SHEET_LONG = 3508
SHEET_SHORT = 2480


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
    def extension(string: str):
        return string.strip(".")

    chart_parser = argparse.ArgumentParser(
        prog=f"phlogiston {AVAILABLE_COMMANDS[0]}",
        description="Fantasy Starchart mapper from input file",
    )
    chart_parser.add_argument("filename")
    chart_parser.add_argument("--dimensions", "-n", default=2, type=int)
    chart_parser.add_argument("--radius", "-r", default=0.2, type=float)
    chart_parser.add_argument("--distance_metric", "-p", default=0.1, type=float)
    chart_parser.add_argument("--name", "-s", default="", type=str)
    chart_parser.add_argument("--dtime", "-t", default=1, type=float)
    chart_parser.add_argument("--output", "-o", default="/")
    chart_parser.add_argument(
        "--extension", "-e", type=extension, choices=EXTENSIONS_OUT, default="html"
    )

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
        outf = return_outputname(cargs.filename, cargs.output, cargs.extension)

        chart_from_file(
            cargs.filename,
            outf,
            cargs.extension,
            cargs.dimensions,
            cargs.radius,
            cargs.distance_metric,
            cargs.name,
            cargs.dtime,
        )


def chart_from_file(filename, foutname, ext, n, radius, p, name, dtime):
    ls = ph.list_spheres(filename)
    sphere_n = {l.sphere_no: l.name for l in ls}
    net = ph.create_network(ls, n, radius, p)
    fig = plot_graph(net, sphere_n, map_name=name, distance_corr=dtime)

    if ext == "html":
        fig.write_html(foutname)
        return foutname

    if importlib.util.find_spec("kaleido") is None:
        log.error(
            "Saving the chart as png/pdf requires the kaleido python package. Please run:\npip install -U kaleido"
        )

    if ext == "pdf":
        # write garbage graph, to get rid of loading bar bug in kaleido
        import plotly.express as px
        import time

        gfig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
        gfig.write_image(foutname, format="pdf")
        time.sleep(2)

        # TODO Change layout to be more printer friendly
        make_printer_friendly(fig).write_image(
            foutname,
            format="pdf",
            width=SHEET_LONG,
            height=SHEET_SHORT,
            scale=2
        )
    elif ext == "png":
        fig.write_image(foutname, format="png")
    return foutname


def generate_random_chart():
    pass


if __name__ == "__main__":
    main()
