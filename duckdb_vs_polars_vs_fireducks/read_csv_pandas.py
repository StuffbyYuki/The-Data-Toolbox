import pandas as pd

def read_csv_pandas(file_path):
    return pd.read_csv(file_path, engine='pyarrow', dtype_backend='pyarrow')

if __name__ == '__main__':
    print(read_csv_pandas('data/2021_Yellow_Taxi_Trip_Data.csv')) 