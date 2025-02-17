import duckdb
from config import DATA_FILE_PATH_STR, DUCKDB_DTYPES


def agg_duckdb(file_path):
    query = f"""
        select 
            sum(total_amount),
            avg(total_amount),
            min(total_amount),
            max(total_amount)
        from read_csv("{file_path}", columns={DUCKDB_DTYPES})
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(agg_duckdb(DATA_FILE_PATH_STR))
