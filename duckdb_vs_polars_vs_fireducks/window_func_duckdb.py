import duckdb
from config import get_data_file_path_str
from utils import read_data_duckdb


def window_func_duckdb(file_path):
    query = f"""
        select 
            dense_rank() over(partition by payment_type order by total_amount desc) 
        from {read_data_duckdb(file_path)}
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(window_func_duckdb(get_data_file_path_str("parquet")))
