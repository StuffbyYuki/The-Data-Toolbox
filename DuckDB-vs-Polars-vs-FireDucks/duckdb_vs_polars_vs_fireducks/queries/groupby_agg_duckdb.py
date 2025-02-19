import duckdb
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_duckdb


def groupby_agg_duckdb(file_path):
    query = f"""
        select 
            VendorID,
            payment_type,
            sum(total_amount),
            avg(total_amount),
            min(total_amount),
            max(total_amount)
        from {read_data_duckdb(file_path)}
        group by
            VendorID,
            payment_type
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(groupby_agg_duckdb(get_data_file_path_str("parquet"))) 