import os
import pytest
import polars as pl
from polars.testing import assert_frame_equal
from duckdb_vs_polars_vs_fireducks.config import DATASET_NAME, POLARS_DTYPES
from duckdb_vs_polars_vs_fireducks.queries.agg_duckdb import agg_duckdb
from duckdb_vs_polars_vs_fireducks.queries.agg_polars import agg_polars
from duckdb_vs_polars_vs_fireducks.queries.agg_fireducks import agg_fireducks
from duckdb_vs_polars_vs_fireducks.queries.groupby_agg_duckdb import groupby_agg_duckdb
from duckdb_vs_polars_vs_fireducks.queries.groupby_agg_polars import groupby_agg_polars
from duckdb_vs_polars_vs_fireducks.queries.groupby_agg_fireducks import (
    groupby_agg_fireducks,
)
from duckdb_vs_polars_vs_fireducks.queries.window_func_duckdb import window_func_duckdb
from duckdb_vs_polars_vs_fireducks.queries.window_func_polars import window_func_polars
from duckdb_vs_polars_vs_fireducks.queries.window_func_fireducks import (
    window_func_fireducks,
)
from duckdb_vs_polars_vs_fireducks.queries.join_duckdb import join_duckdb
from duckdb_vs_polars_vs_fireducks.queries.join_polars import join_polars
from duckdb_vs_polars_vs_fireducks.queries.join_fireducks import join_fireducks


@pytest.fixture(scope="module")
def test_data():
    """Creates a limited test dataset that all tests will use.

    The scope="module" ensures this fixture runs once per test module
    rather than for each test function.
    """
    # Read and limit the data
    df = (
        pl.scan_csv(f"data/{DATASET_NAME}.csv", schema=POLARS_DTYPES)
        .head(1000)
        .collect()
    )

    # Save to a temporary parquet file for testing
    test_file = "data/test_data.parquet"
    df.write_parquet(test_file)

    yield test_file  # provide the test file path to the tests

    # Cleanup after all tests complete
    if os.path.exists(test_file):
        os.remove(test_file)


def test_agg(test_data):
    """Tests aggregation operations across Polars, DuckDB, and FireDucks."""
    polars_result = agg_polars(test_data)
    duckdb_result = agg_duckdb(test_data)
    fireducks_result = agg_fireducks(test_data).to_frame().T.reset_index(drop=True)

    assert_frame_equal(
        polars_result,
        pl.from_arrow(duckdb_result),
        check_row_order=False,
        check_dtypes=False,
    )
    assert_frame_equal(
        polars_result,
        pl.from_arrow(fireducks_result),
        check_row_order=False,
        check_dtypes=False,
    )


def test_groupby_agg(test_data):
    """Tests groupby aggregation operations across Polars, DuckDB, and FireDucks."""
    polars_result = groupby_agg_polars(test_data)
    duckdb_result = groupby_agg_duckdb(test_data)
    fireducks_result = (
        groupby_agg_fireducks(test_data).rename(columns={"mean": "avg"}).reset_index()
    )

    assert_frame_equal(
        polars_result,
        pl.from_arrow(duckdb_result),
        check_row_order=False,
        check_dtypes=False,
    )
    assert_frame_equal(
        polars_result,
        pl.from_arrow(fireducks_result),
        check_row_order=False,
        check_dtypes=False,
    )


def test_window_func(test_data):
    """Tests window function operations across Polars, DuckDB, and FireDucks."""
    polars_result = window_func_polars(test_data)
    duckdb_result = window_func_duckdb(test_data)
    fireducks_result = window_func_fireducks(test_data)

    assert_frame_equal(
        polars_result,
        pl.from_arrow(duckdb_result),
        check_row_order=False,
        check_dtypes=False,
    )
    assert_frame_equal(
        polars_result,
        pl.from_arrow(fireducks_result),
        check_row_order=False,
        check_dtypes=False,
    )


def test_join(test_data):
    """Tests join operations across Polars, DuckDB, and FireDucks."""
    polars_result = join_polars(test_data)
    duckdb_result = join_duckdb(test_data)
    fireducks_result = join_fireducks(test_data)

    assert_frame_equal(
        polars_result,
        pl.from_arrow(duckdb_result),
        check_row_order=False,
        check_dtypes=False,
    )
    assert_frame_equal(
        polars_result,
        pl.from_arrow(fireducks_result),
        check_row_order=False,
        check_dtypes=False,
    )
