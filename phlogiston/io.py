import os
import logging
import numpy as np
import pandas as pd

COLNAMES = ["sphere", "desc", "x", "y", "z"]
DTYPES = [np.str_, np.str_, np.float32, np.float32, np.float32]
DDTYPE = {k: v for k, v in zip(COLNAMES, DTYPES)}
log = logging.getLogger("phlogiston")


def spheres_csv_to_df(filename):
    return pd.read_csv(
        filename,
        header=0,
        dtype=DDTYPE,
        names=COLNAMES,
    )


def spheres_tsv_to_df(filename):
    return pd.read_table(filename, header=0, dtype=DDTYPE, names=COLNAMES)


def spheres_excel_to_df(filename):
    return pd.read_excel(filename, header=0, dtype=DDTYPE, names=COLNAMES)


READERS = dict(csv=spheres_csv_to_df, tsv=spheres_tsv_to_df, xlsx=spheres_excel_to_df)


def read_spheres(filename):

    ext = os.path.splitext(filename)[-1].strip(".")
    if ext in READERS:
        return READERS[ext](filename)
    else:
        logging.error(f"{ext} format of {filename} not supported.")


def return_outputname(fin, fout, ext):

    if fout == "/":
        fout = os.path.splitext(os.path.basename(fin))[0]
    else:
        fout, ext_f = os.path.splitext(fout)
        if ext_f != "":
            return "".join(fout, ext_f)

    return f"{fout}.{ext}"
