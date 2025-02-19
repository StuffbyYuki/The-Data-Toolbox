import pytest
import polars as pl
import duckdb
from polars.testing import assert_frame_equal
from duckdb_vs_polars_vs_fireducks.config import DATASET_NAME, POLARS_DTYPES
import pandas as pd


@pytest.fixture
def df():
    """
    Creates a base Polars DataFrame that all tests will use.
    """
    # Polars code
    return pl.scan_csv(f"data/{DATASET_NAME}.csv", schema=POLARS_DTYPES).head(1000).collect()


def test_agg(df):
    """
    Tests aggregation operations across Polars, DuckDB, and Pandas.
    """
    # Polars code
    polars_df = df.select(
        sum=pl.col("total_amount").sum(),
        avg=pl.col("total_amount").mean(),
        min=pl.col("total_amount").min(),
        max=pl.col("total_amount").max(),
    )

    # DuckDB code
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

    # Pandas code
    pandas_df = (
        df.to_pandas()["total_amount"]
        .agg({"sum": "sum", "avg": "mean", "min": "min", "max": "max"})
        .to_frame()
        .T
    )

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False, check_dtypes=False)
    assert_frame_equal(
        polars_df, pl.from_pandas(pandas_df), check_row_order=False, check_dtypes=False
    )


def test_groupby_agg(df):
    """
    Tests groupby aggregation operations across Polars, DuckDB, and Pandas.
    """
    group_cols = ["VendorID", "payment_type"]
    # Polars code
    polars_df = df.group_by(group_cols).agg(
        sum=pl.col("total_amount").sum(),
        avg=pl.col("total_amount").mean(),
        min=pl.col("total_amount").min(),
        max=pl.col("total_amount").max(),
    )
    print(polars_df.head())

    # DuckDB code
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

    # Pandas code
    pandas_df = (
        df.to_pandas()
        .groupby(["VendorID", "payment_type"])["total_amount"]
        .agg(["sum", "mean", "min", "max"])
        .rename(columns={"mean": "avg"})
        .reset_index()
    )

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False, check_dtypes=False)
    assert_frame_equal(
        polars_df, pl.from_pandas(pandas_df), check_row_order=False, check_dtypes=False
    )


def test_window_func(df):
    """
    Tests window function operations across Polars, DuckDB, and Pandas.
    """
    # Polars code
    polars_df = df.select(
        avg_fare_per_vendor=pl.col("fare_amount").mean().over("VendorID"),
        ttl_amt_rank_per_pay_type=pl.col("total_amount")
        .rank(method="dense", descending=True)
        .over("payment_type"),
    )

    # DuckDB code
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
        .with_columns(pl.col("ttl_amt_rank_per_pay_type"))
    )

    # Pandas code
    pandas_df = pd.DataFrame(
        {
            "avg_fare_per_vendor": df.to_pandas()
            .groupby("VendorID")["fare_amount"]
            .transform("mean"),
            "ttl_amt_rank_per_pay_type": df.to_pandas()
            .groupby("payment_type")["total_amount"]
            .rank(method="dense", ascending=False),
        }
    )

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False, check_dtypes=False)
    assert_frame_equal(
        polars_df, pl.from_pandas(pandas_df), check_row_order=False, check_dtypes=False
    )


def test_join(df):
    """
    Tests join operations across Polars, DuckDB, and Pandas.
    """
    base_df = df.with_columns(
        pl.col("tpep_pickup_datetime")
        .str.to_datetime("%m/%d/%Y %I:%M:%S %p")
        .dt.month()
        .alias("pickup_month")
    )
    join_df = base_df.group_by("VendorID", "payment_type", "pickup_month").agg(
        sum=pl.col("total_amount").sum()
    )
    # Polars code
    polars_df = base_df.join(
        join_df, on=["VendorID", "payment_type", "pickup_month"], how="inner"
    )

    # DuckDB code
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

    # Pandas code
    pdf = df.to_pandas()
    pdf["pickup_month"] = pd.to_datetime(
        pdf["tpep_pickup_datetime"], format="%m/%d/%Y %I:%M:%S %p"
    ).dt.month

    agg_df = (
        pdf.groupby(["VendorID", "payment_type", "pickup_month"])["total_amount"]
        .sum()
        .reset_index()
    )
    agg_df.columns = ["VendorID", "payment_type", "pickup_month", "sum"]

    pandas_df = pdf.merge(
        agg_df, on=["VendorID", "payment_type", "pickup_month"], how="inner"
    )

    assert_frame_equal(polars_df, duckdb_df, check_row_order=False, check_dtypes=False)
    assert_frame_equal(
        polars_df, pl.from_pandas(pandas_df), check_row_order=False, check_dtypes=False
    )
