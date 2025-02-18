import fireducks.pandas as pd
from config import DATA_FILE_PATH_STR, PANDAS_DTYPES


def read_csv_fireducks(file_path):
    return pd.read_csv(
        file_path, engine="pyarrow", dtype_backend="pyarrow", dtype=PANDAS_DTYPES
    )


if __name__ == "__main__":
    print(read_csv_fireducks(DATA_FILE_PATH_STR)) 