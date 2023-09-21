import os
import logging
import numpy as np
import pandas as pd
from functools import partial

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

def spheres_df_to_csv(df:pd.DataFrame, filename, sep=","):
    df.to_csv(filename, sep=sep, index=False)


def spheres_df_to_xlsx(df:pd.DataFrame, filename):
    df.to_excel(filename, index=False)

WRITERS = dict(csv=spheres_df_to_csv, tsv=partial(spheres_df_to_csv, sep="\t"), xlsx=spheres_df_to_xlsx)


def read_spheres(filename):

    ext = os.path.splitext(filename)[-1].strip(".")
    if ext in READERS:
        return READERS[ext](filename)
    else:
        logging.error(f"{ext} format of {filename} not supported.")


def write_spheres(sphere_list, filename):
    df = pd.concat([sp.to_row() for sp in sphere_list], axis=0)
    ext = os.path.splitext(filename)[-1].strip(".")
    if ext in WRITERS:
        return WRITERS[ext](df, filename)
    else:
        logging.error(f"{ext} format of {filename} not supported.")



def return_outputname(fin, fout, ext):

    if fout == "/":
        fout = os.path.splitext(os.path.basename(fin))[0]
    else:
        fout, ext_f = os.path.splitext(fout)
        if ext_f != "":
            return "".join([fout, ext_f])

    return f"{fout}.{ext}"
