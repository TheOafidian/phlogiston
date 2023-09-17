import os
import pytest
import filetype
from phlogiston.cli import chart_from_file, EXTENSIONS_OUT
from phlogiston.io import READERS


def test_chart_to_extensions(tmp_path):

    for ext_out, ext_in in zip(EXTENSIONS_OUT, READERS):
        outf = tmp_path / f"test.{ext_out}"
        chart_from_file(
            f"tests/data/example-planes.{ext_in}", outf, ext_out, 
            2, 0.2, 0.1, "", 1)
        if ext_out == "html":
            assert outf.read_text().startswith("<html>")
        else:
            assert filetype.guess(outf).extension == ext_out



