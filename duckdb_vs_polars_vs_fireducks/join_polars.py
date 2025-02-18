import polars as pl
from config import get_data_file_path_str
from utils import read_data_polars


def join_polars(file_path):
    base_lf = read_data_polars(file_path).with_columns(
        pl.col("tpep_pickup_datetime")
        .str.to_datetime("%m/%d/%Y %I:%M:%S %p")
        .dt.month()
        .alias("pickup_month")
    )
    join_lf = base_lf.group_by("VendorID", "payment_type", "pickup_month").agg(
        sum=pl.col("total_amount").sum()
    )
    return base_lf.join(
        join_lf, on=["VendorID", "payment_type", "pickup_month"], how="inner"
    ).collect()


if __name__ == "__main__":
    print(join_polars(get_data_file_path_str("parquet")))
