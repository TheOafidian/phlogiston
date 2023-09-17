import os
import pytest
import filetype
from phlogiston.cli import main, EXTENSIONS_OUT
from phlogiston.io import READERS



@pytest.mark.parametrize("args", ("-h", "--help"))
def test_help_page(capsys, args):

    with pytest.raises(SystemExit):
        main(args=[args])
    output = capsys.readouterr().out
    assert "usage: phlogiston [-h] {chart,random}" in output


def test_file_ext_outputs(tmp_path):
    for ext_out, ext_in in zip(EXTENSIONS_OUT, READERS):
        outf = tmp_path / f"test.{ext_out}"

        main([
            "chart",
            f"tests/data/example-planes.{ext_in}", 
            f"-o{str(outf)}", f"-e{ext_out}"])
        if ext_out == "html":
            assert outf.read_text().startswith("<html>")
        else:
            assert filetype.guess(outf).extension == ext_out



