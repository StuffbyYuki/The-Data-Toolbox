import pandas as pd
from config import DATA_FILE_PATH_STR, PANDAS_DTYPES


def agg_pandas(file_path):
    df = pd.read_csv(
        file_path,
        engine="pyarrow",
        dtype_backend="pyarrow",
        dtype=PANDAS_DTYPES,
    )
    return df["total_amount"].agg(["sum", "mean", "min", "max"])


if __name__ == "__main__":
    print(agg_pandas(DATA_FILE_PATH_STR))
