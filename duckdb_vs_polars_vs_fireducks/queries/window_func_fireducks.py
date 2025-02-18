import fireducks.pandas as pd
from duckdb_vs_polars_vs_fireducks.config import get_data_file_path_str
from duckdb_vs_polars_vs_fireducks.utils import read_data_fireducks


def window_func_fireducks(file_path):
    df = read_data_fireducks(file_path)
    return pd.DataFrame(
        {
            "ttl_amt_rank_per_pay_type": df.groupby("payment_type")[
                "total_amount"
            ].rank(method="dense", ascending=False),
        }
    )._evaluate()


if __name__ == "__main__":
    print(window_func_fireducks(get_data_file_path_str("parquet"))) 