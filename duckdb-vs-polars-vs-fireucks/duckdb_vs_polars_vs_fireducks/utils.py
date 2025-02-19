import polars as pl
import fireducks.pandas as pd
from duckdb_vs_polars_vs_fireducks.config import (
    DUCKDB_DTYPES,
    POLARS_DTYPES,
    PANDAS_DTYPES,
)


def read_data_duckdb(file_path):
    """Generate DuckDB query to read either CSV or parquet file."""
    is_csv = file_path.endswith(".csv")
    return (
        'read_csv("' + file_path + '", columns=' + str(DUCKDB_DTYPES) + ")"
        if is_csv
        else 'read_parquet("' + file_path + '")'
    )


def read_data_polars(file_path):
    """Read file with Polars using appropriate method based on file type."""
    if file_path.endswith(".csv"):
        return pl.scan_csv(file_path, schema=POLARS_DTYPES)
    return pl.scan_parquet(file_path)


def read_data_fireducks(file_path):
    """Read file with Fireducks using appropriate method based on file type."""
    if file_path.endswith(".csv"):
        return pd.read_csv(
            file_path, engine="pyarrow", dtype_backend="pyarrow", dtype=PANDAS_DTYPES
        )
    return pd.read_parquet(file_path)
