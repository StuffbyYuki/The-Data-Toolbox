import polars as pl
from config import DATA_FILE_PATH_STR, POLARS_DTYPES


def window_func_polars(file_path):
    lf = pl.scan_csv(file_path, schema=POLARS_DTYPES)
    return lf.select(
        ttl_amt_rank_per_pay_type=pl.col("total_amount")
        .rank(method="dense", descending=True)
        .over("payment_type"),
    ).collect()


if __name__ == "__main__":
    print(window_func_polars(DATA_FILE_PATH_STR))
