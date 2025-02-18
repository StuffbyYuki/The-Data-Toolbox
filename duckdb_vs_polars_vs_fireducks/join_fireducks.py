import fireducks.pandas as pd
from config import get_data_file_path_str
from utils import read_data_fireducks


def join_fireducks(file_path):
    df = read_data_fireducks(file_path)
    df["pickup_month"] = pd.to_datetime(
        df["tpep_pickup_datetime"], format="%m/%d/%Y %I:%M:%S %p"
    ).dt.month

    agg_df = (
        df.groupby(["VendorID", "payment_type", "pickup_month"])["total_amount"]
        .sum()
        .reset_index()
    )
    agg_df.columns = ["VendorID", "payment_type", "pickup_month", "sum"]

    return df.merge(
        agg_df, on=["VendorID", "payment_type", "pickup_month"], how="inner"
    )._evaluate()


if __name__ == "__main__":
    print(join_fireducks(get_data_file_path_str("parquet")))
