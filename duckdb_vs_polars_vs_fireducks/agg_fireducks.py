from config import get_data_file_path_str
from utils import read_data_fireducks


def agg_fireducks(file_path):
    df = read_data_fireducks(file_path)
    return df["total_amount"].agg(["sum", "mean", "min", "max"])._evaluate()


if __name__ == "__main__":
    print(agg_fireducks(get_data_file_path_str("parquet")))
