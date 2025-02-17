import pandas as pd
from config import DATA_FILE_PATH_STR, PANDAS_DTYPES


def window_func_pandas(file_path):
    df = pd.read_csv(file_path, engine="pyarrow", dtype_backend="pyarrow", dtype=PANDAS_DTYPES)
    return pd.DataFrame(
        {
            "avg_fare_per_vendor": df.groupby("VendorID")["fare_amount"].transform(
                "mean"
            ),
            "ttl_amt_rank_per_pay_type": df.groupby("payment_type")[
                "total_amount"
            ].rank(method="dense", ascending=False),
        }
    )


if __name__ == "__main__":
    print(window_func_pandas(DATA_FILE_PATH_STR))
