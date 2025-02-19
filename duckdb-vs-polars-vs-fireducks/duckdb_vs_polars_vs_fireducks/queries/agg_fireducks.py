from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_fireducks


def agg_fireducks(file_path):
    df = read_data_fireducks(file_path)
    return df["total_amount"].agg({"sum": "sum", "avg": "mean", "min": "min", "max": "max"})._evaluate()


if __name__ == "__main__":
    print(agg_fireducks(get_data_file_path_str("parquet"))) 