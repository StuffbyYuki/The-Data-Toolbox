import pandas as pd

def join_pandas(file_path):
    df = pd.read_csv(file_path, engine='pyarrow', dtype_backend='pyarrow')
    df['pickup_month'] = pd.to_datetime(df['tpep_pickup_datetime'], format='%m/%d/%Y %I:%M:%S %p').dt.month
    
    agg_df = df.groupby(['VendorID', 'payment_type', 'pickup_month'])['total_amount'].sum().reset_index()
    agg_df.columns = ['VendorID', 'payment_type', 'pickup_month', 'sum']
    
    return df.merge(
        agg_df,
        on=['VendorID', 'payment_type', 'pickup_month'],
        how='inner'
    )

if __name__ == '__main__':
    print(join_pandas('data/2021_Yellow_Taxi_Trip_Data.csv')) 