import pandas as pd
from config import DATA_FILE_PATH_STR
def read_csv_pandas(file_path):
    return pd.read_csv(file_path, engine='pyarrow', dtype_backend='pyarrow')

if __name__ == '__main__':
    print(read_csv_pandas(DATA_FILE_PATH_STR)) 