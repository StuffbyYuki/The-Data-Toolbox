"""Configuration settings for the benchmark."""

from pathlib import Path
import polars as pl

# Base data directory
DATA_DIR = Path("data")

# Main data file path
DATA_FILE_PATH = DATA_DIR / "2023_Yellow_Taxi_Trip_Data.csv"

# Convert to string for compatibility with all libraries
DATA_FILE_PATH_STR = str(DATA_FILE_PATH)

# Schema definitions for each library
PANDAS_DTYPES = {
    "VendorID": "Int64",
    "tpep_pickup_datetime": "string",
    "tpep_dropoff_datetime": "string",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "airport_fee": "float64",
}

POLARS_DTYPES = {
    "VendorID": pl.Int64,
    "tpep_pickup_datetime": pl.String,
    "tpep_dropoff_datetime": pl.String,
    "passenger_count": pl.Int64,
    "trip_distance": pl.Float64,
    "RatecodeID": pl.Int64,
    "store_and_fwd_flag": pl.String,
    "PULocationID": pl.Int64,
    "DOLocationID": pl.Int64,
    "payment_type": pl.Int64,
    "fare_amount": pl.Float64,
    "extra": pl.Float64,
    "mta_tax": pl.Float64,
    "tip_amount": pl.Float64,
    "tolls_amount": pl.Float64,
    "improvement_surcharge": pl.Float64,
    "total_amount": pl.Float64,
    "congestion_surcharge": pl.Float64,
    "airport_fee": pl.Float64,
}

DUCKDB_DTYPES = {
    "VendorID": "INT64",
    "tpep_pickup_datetime": "STRING",
    "tpep_dropoff_datetime": "STRING",
    "passenger_count": "INT64",
    "trip_distance": "DOUBLE",
    "RatecodeID": "INT64",
    "store_and_fwd_flag": "STRING",
    "PULocationID": "INT64",
    "DOLocationID": "INT64",
    "payment_type": "INT64",
    "fare_amount": "DOUBLE",
    "extra": "DOUBLE",
    "mta_tax": "DOUBLE",
    "tip_amount": "DOUBLE",
    "tolls_amount": "DOUBLE",
    "improvement_surcharge": "DOUBLE",
    "total_amount": "DOUBLE",
    "congestion_surcharge": "DOUBLE",
    "airport_fee": "DOUBLE",
}
