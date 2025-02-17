import duckdb
from config import DATA_FILE_PATH_STR, DUCKDB_DTYPES


def groupby_agg_duckdb(file_path):
    query = f"""
        select 
            VendorID,
            payment_type,
            sum(total_amount),
            avg(total_amount),
            min(total_amount),
            max(total_amount)
        from read_csv("{file_path}", columns={DUCKDB_DTYPES})
        group by
            VendorID,
            payment_type
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(groupby_agg_duckdb(DATA_FILE_PATH_STR))
