import polars as pl
from config import DATA_FILE_PATH_STR, POLARS_DTYPES


def read_csv_polars(file_path):
    lf = pl.scan_csv(file_path, schema=POLARS_DTYPES)
    return lf.collect()


if __name__ == "__main__":
    print(read_csv_polars(DATA_FILE_PATH_STR))
