import duckdb
from config import DATA_FILE_PATH_STR, DUCKDB_DTYPES


def read_csv_duckdb(file_path):
    query = f"""
        select * from read_csv("{file_path}", columns={DUCKDB_DTYPES})";
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(read_csv_duckdb(DATA_FILE_PATH_STR))
