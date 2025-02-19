import duckdb
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_duckdb


def groupby_agg_duckdb(file_path):
    query = f"""
        select 
            VendorID,
            payment_type,
            sum(total_amount) sum,
            avg(total_amount) avg,
            min(total_amount) min,
            max(total_amount) max
        from {read_data_duckdb(file_path)}
        group by
            VendorID,
            payment_type
        ;
    """
    return duckdb.sql(query).arrow()


if __name__ == "__main__":
    print(groupby_agg_duckdb(get_data_file_path_str("parquet"))) 