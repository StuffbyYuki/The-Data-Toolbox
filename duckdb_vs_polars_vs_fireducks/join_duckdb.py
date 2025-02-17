import duckdb
from config import DATA_FILE_PATH_STR, DUCKDB_DTYPES


def join_duckdb(file_path):
    query = f"""

        with source as (
            select *
            from read_csv("{file_path}", columns={DUCKDB_DTYPES})
        ),
        
        base as (
            select 
                *,
                EXTRACT(MONTH FROM STRPTIME(tpep_pickup_datetime, '%m/%d/%Y %I:%M:%S %p')) AS pickup_month,
            from source
        ),
        
        join_data as (
            select 
                VendorID,
                payment_type,
                pickup_month,
                sum(total_amount)
            from base
            group by
                VendorID,
                payment_type,
                pickup_month
        )
            
        select *
        from base
        inner join join_data
            using (VendorID, payment_type, pickup_month) 
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(join_duckdb(DATA_FILE_PATH_STR))
