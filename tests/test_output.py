import pytest
import polars as pl
import duckdb
from polars.testing import assert_frame_equal
from duckdb_vs_polars_vs_fireducks.config import DATA_FILE_PATH_STR, POLARS_DTYPES
import pandas as pd


@pytest.fixture
def df():
    # Create base Polars DataFrame that all tests will use
    return pl.scan_csv(DATA_FILE_PATH_STR, schema=POLARS_DTYPES).head(1000).collect()



def test_agg(df):
    polars_df = df.select(
        sum=pl.col("total_amount").sum(),
        avg=pl.col("total_amount").mean(),
        min=pl.col("total_amount").min(),
        max=pl.col("total_amount").max(),
    )
    query = f"""
        select 
            sum(total_amount) sum,
            avg(total_amount) avg,
            min(total_amount) min,
            max(total_amount) max
        from df
        ;
    """
    duckdb_df = duckdb.sql(query).pl()

    assert_frame_equal(polars_df, duckdb_df)


def test_groupby_agg(df):
    group_cols = ["VendorID", "payment_type"]
    polars_df = df.group_by(group_cols).agg(
        sum=pl.col("total_amount").sum(),
        avg=pl.col("total_amount").mean(),
        min=pl.col("total_amount").min(),
        max=pl.col("total_amount").max(),
    )
    print(polars_df.head())
    query = f"""
        select 
            VendorID,
            payment_type,
            sum(total_amount) sum,
            avg(total_amount) avg,
            min(total_amount) min,
            max(total_amount) max
        from df
        group by
            VendorID,
            payment_type
        order by 
            VendorID,
            payment_type
        ;
    """
    duckdb_df = duckdb.sql(query).pl()

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False)


def test_window_func(df):
    polars_df = df.select(
        avg_fare_per_vendor=pl.col("fare_amount").mean().over("VendorID"),
        ttl_amt_rank_per_pay_type=pl.col("total_amount")
        .rank(method="dense", descending=True)
        .over("payment_type"),
    )
    query = f"""
        select 
            avg(fare_amount) over(partition by VendorID) avg_fare_per_vendor,
            dense_rank() over(partition by payment_type order by total_amount desc) ttl_amt_rank_per_pay_type 
        from df
        ;
    """
    duckdb_df = (
        duckdb.sql(query)
        .pl()
        .with_columns(pl.col("ttl_amt_rank_per_pay_type").cast(pl.UInt32))
    )

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False)


def test_join(df):
    base_df = df.with_columns(
        pl.col("tpep_pickup_datetime")
        .str.to_datetime("%m/%d/%Y %I:%M:%S %p")
        .dt.month()
        .alias("pickup_month")
    )
    join_df = base_df.group_by("VendorID", "payment_type", "pickup_month").agg(
        sum=pl.col("total_amount").sum()
    )
    polars_df = base_df.join(
        join_df, on=["VendorID", "payment_type", "pickup_month"], how="inner"
    )

    query = f"""

        with join_data as (
            select 
                VendorID,
                payment_type,
                pickup_month,
                sum(total_amount) sum
            from base_df
            group by
                VendorID,
                payment_type,
                pickup_month
        )
            
        select *
        from base_df
        inner join join_data
            using (VendorID, payment_type, pickup_month) 
        ;
    """
    duckdb_df = duckdb.sql(query).pl()

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False)
