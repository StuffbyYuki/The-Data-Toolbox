import polars as pl 
from config import DATA_FILE_PATH_STR
def groupby_agg_polars(file_path):
    lf = pl.scan_csv(file_path)
    return (
        lf
        .group_by('VendorID', 'payment_type')
        .agg(
            sum=pl.col('total_amount').sum(),
            avg=pl.col('total_amount').mean(),
            min=pl.col('total_amount').min(),
            max=pl.col('total_amount').max()
        )
        .collect()
    )

if __name__ == '__main__':
    print(groupby_agg_polars(DATA_FILE_PATH_STR))