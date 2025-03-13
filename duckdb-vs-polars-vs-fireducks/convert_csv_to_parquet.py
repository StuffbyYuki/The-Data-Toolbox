import polars as pl


CSV_FILE_PATH = 'data/2023_Yellow_Taxi_Trip_Data.csv'
PARQUET_FILE_PATH = 'data/2023_Yellow_Taxi_Trip_Data.parquet'

def convert_csv_to_parquet(csv_file_path, parquet_file_path, row_group_size=1_000_000):
    df = pl.scan_csv(csv_file_path, infer_schema_length=100000)
    df.collect().write_parquet(parquet_file_path, row_group_size=row_group_size)

if __name__ == "__main__":
    convert_csv_to_parquet(
        csv_file_path=CSV_FILE_PATH, 
        parquet_file_path=PARQUET_FILE_PATH
    )
