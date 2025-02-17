import pytest
import polars as pl
import duckdb
from polars.testing import assert_frame_equal
from duckdb_vs_polars_vs_fireducks.config import DATA_FILE_PATH_STR, POLARS_DTYPES

@pytest.fixture
def lf():
    return pl.scan_csv(DATA_FILE_PATH_STR, schema=POLARS_DTYPES).head(1000)

def test_agg(lf):
    polars_df = (
        lf
        .select(
            sum=pl.col('total_amount').sum(),
            avg=pl.col('total_amount').mean(),
            min=pl.col('total_amount').min(),
            max=pl.col('total_amount').max()
        )
        .collect()
    )
    query = f'''
        select 
            sum(total_amount) sum,
            avg(total_amount) avg,
            min(total_amount) min,
            max(total_amount) max
        from lf
        ;
    '''
    duckdb_df = duckdb.sql(query).pl()

    assert_frame_equal(polars_df, duckdb_df)

def test_groupby_agg(lf):
    group_cols = ['VendorID', 'payment_type']
    polars_df = (
        lf
        .group_by(group_cols)
        .agg(
            sum=pl.col('total_amount').sum(),
            avg=pl.col('total_amount').mean(),
            min=pl.col('total_amount').min(),
            max=pl.col('total_amount').max()
        )
        .collect()
    )
    print(polars_df.head())
    query = f'''
        select 
            VendorID,
            payment_type,
            sum(total_amount) sum,
            avg(total_amount) avg,
            min(total_amount) min,
            max(total_amount) max
        from lf
        group by
            VendorID,
            payment_type
        order by 
            VendorID,
            payment_type
        ;
    '''
    duckdb_df = duckdb.sql(query).pl()
    
    assert_frame_equal(polars_df, duckdb_df, check_row_order=False)

def test_window_func(lf):
    polars_df = (
        lf
        .select(
            avg_fare_per_vendor=pl.col('fare_amount').mean().over('VendorID'),
            ttl_amt_rank_per_pay_type=pl.col('total_amount').rank(method='dense', descending=True).over('payment_type')
        )
        .collect()
    )
    query = f'''
        select 
            avg(fare_amount) over(partition by VendorID) avg_fare_per_vendor,
            dense_rank() over(partition by payment_type order by total_amount desc) ttl_amt_rank_per_pay_type 
        from lf
        ;
    '''
    duckdb_df = duckdb.sql(query).pl().with_columns(pl.col('ttl_amt_rank_per_pay_type').cast(pl.UInt32))

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False)

def test_join(lf):
    base_lf = (
        lf
        .with_columns(
            pl.col('tpep_pickup_datetime').str.to_datetime('%m/%d/%Y %I:%M:%S %p')
            .dt.month()
            .alias('pickup_month')
        )
    )
    join_lf = (
        base_lf
        .group_by('VendorID', 'payment_type', 'pickup_month')
        .agg(
            sum=pl.col('total_amount').sum()
        )   
    )
    polars_df = (
        base_lf
        .join(
            join_lf,
            on=['VendorID', 'payment_type', 'pickup_month'], 
            how='inner'
        )
        .collect()
    )

    query = f'''

        with join_data as (
            select 
                VendorID,
                payment_type,
                pickup_month,
                sum(total_amount) sum
            from base_lf
            group by
                VendorID,
                payment_type,
                pickup_month
        )
            
        select *
        from base_lf
        inner join join_data
            using (VendorID, payment_type, pickup_month) 
        ;
    '''
    duckdb_df = duckdb.sql(query).pl()

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False)
