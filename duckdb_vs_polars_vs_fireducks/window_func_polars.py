import polars as pl 

def window_func_polars(file_path):
    lf = pl.scan_csv(file_path)
    return (
        lf
        .select(
            avg_fare_per_vendor=pl.col('fare_amount').mean().over('VendorID'),
            ttl_amt_rank_per_pay_type=pl.col('total_amount').rank(method='dense', descending=True).over('payment_type')
        )
        .collect()
    )

if __name__ == '__main__':
    print(window_func_polars('data/2021_Yellow_Taxi_Trip_Data.csv'))