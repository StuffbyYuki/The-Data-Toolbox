import polars as pl
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_polars


def groupby_agg_polars(file_path):
    lf = read_data_polars(file_path)
    return (
        lf.group_by("VendorID", "payment_type")
        .agg(
            sum=pl.col("total_amount").sum(),
            avg=pl.col("total_amount").mean(),
            min=pl.col("total_amount").min(),
            max=pl.col("total_amount").max(),
        )
        .collect()
    )


if __name__ == "__main__":
    print(groupby_agg_polars(get_data_file_path_str("parquet"))) 