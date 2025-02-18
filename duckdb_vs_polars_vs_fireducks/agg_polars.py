import polars as pl
from config import get_data_file_path_str
from utils import read_data_polars


def agg_polars(file_path):
    lf = read_data_polars(file_path)
    return lf.select(
        sum=pl.col("total_amount").sum(),
        avg=pl.col("total_amount").mean(),
        min=pl.col("total_amount").min(),
        max=pl.col("total_amount").max(),
    ).collect()


if __name__ == "__main__":
    print(agg_polars(get_data_file_path_str("parquet")))
