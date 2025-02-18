import duckdb
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_duckdb


def agg_duckdb(file_path):
    query = f"""
        select 
            sum(total_amount),
            avg(total_amount),
            min(total_amount),
            max(total_amount)
        from {read_data_duckdb(file_path)}
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(agg_duckdb(get_data_file_path_str("parquet"))) 