import polars as pl
from config import DATA_FILE_PATH_STR, POLARS_DTYPES


def join_polars(file_path):
    base_lf = pl.scan_csv(
        file_path,
        schema=POLARS_DTYPES,
    ).with_columns(
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
    print(join_polars(DATA_FILE_PATH_STR))
