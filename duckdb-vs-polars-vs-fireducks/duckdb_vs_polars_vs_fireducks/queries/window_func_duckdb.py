import duckdb
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_duckdb


def window_func_duckdb(file_path):
    query = f"""
        select 
            avg(fare_amount) over(partition by VendorID) avg_fare_per_vendor,
            dense_rank() over(partition by payment_type order by total_amount desc) ttl_amt_rank_per_pay_type
        from {read_data_duckdb(file_path)}
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(window_func_duckdb(get_data_file_path_str("parquet"))) 