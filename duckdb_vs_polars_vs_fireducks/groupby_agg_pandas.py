import pandas as pd
from config import DATA_FILE_PATH_STR, PANDAS_DTYPES


def groupby_agg_pandas(file_path):
    df = pd.read_csv(
        file_path, engine="pyarrow", dtype_backend="pyarrow", dtype=PANDAS_DTYPES
    )
    return df.groupby(["VendorID", "payment_type"])["total_amount"].agg(
        ["sum", "mean", "min", "max"]
    )


if __name__ == "__main__":
    print(groupby_agg_pandas(DATA_FILE_PATH_STR))
