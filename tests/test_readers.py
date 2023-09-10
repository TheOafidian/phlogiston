from phlogiston.io import read_spheres, COLNAMES


def test_csv_reader():
    df = read_spheres("tests/data/example-planes.csv")
    assert set(df.columns) == set(COLNAMES)
    assert not df.empty


def test_tsv_reader():
    df = read_spheres("tests/data/example-planes.tsv")
    assert set(df.columns) == set(COLNAMES)
    assert not df.empty


def test_excel_reader():
    df = read_spheres("tests/data/example-planes.xlsx")
    assert set(df.columns) == set(COLNAMES)
    assert not df.empty
