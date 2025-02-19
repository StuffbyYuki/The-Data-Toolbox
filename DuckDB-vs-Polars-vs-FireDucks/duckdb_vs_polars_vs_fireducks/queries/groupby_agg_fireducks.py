from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_fireducks


def groupby_agg_fireducks(file_path):
    df = read_data_fireducks(file_path)
    return (
        df.groupby(["VendorID", "payment_type"])["total_amount"]
        .agg(["sum", "mean", "min", "max"])
        ._evaluate()
    )


if __name__ == "__main__":
    print(groupby_agg_fireducks(get_data_file_path_str("parquet"))) 