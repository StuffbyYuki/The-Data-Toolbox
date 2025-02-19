import polars as pl
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_polars


def window_func_polars(file_path):
    lf = read_data_polars(file_path)
    return lf.select(
        avg_fare_per_vendor=pl.col("fare_amount").mean().over("VendorID"),
        ttl_amt_rank_per_pay_type=pl.col("total_amount")
        .rank(method="dense", descending=True)
        .over("payment_type"),
    ).collect()


if __name__ == "__main__":
    print(window_func_polars(get_data_file_path_str("parquet"))) 