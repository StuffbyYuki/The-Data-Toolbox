# DuckDB vs Polars vs Fireducks Benchmark

A benchmark comparing DuckDB, Polars, and Fireducks (a fork of pandas) for common data operations.

## Project Structure

```
duckdb_vs_polars_vs_fireducks/
├── __init__.py
├── __main__.py
├── config.py
├── utils.py
├── visualize_output.py
└── queries/
    ├── __init__.py
    ├── agg_*.py         # Simple aggregation queries
    ├── groupby_agg_*.py # GroupBy aggregation queries
    ├── join_*.py        # Self-join queries
    └── window_func_*.py # Window function queries
```

## Data
The benchmark uses the [NYC Yellow Taxi Trip Data](https://data.cityofnewyork.us/Transportation/2021-Yellow-Taxi-Trip-Data/m6nq-qud6/about_data) that contains 30M rows with 18 columns. 

Place your data file(s) in the `data` directory:
- Required: `data/2023_Yellow_Taxi_Trip_Data.csv`
- Optional: `data/2023_Yellow_Taxi_Trip_Data.parquet` (if you want to test Parquet format)

The benchmark uses CSV format by default. To run with Parquet format, use the `--file-type parquet` flag.

## Running the Benchmarks

This benchmark is designed to run in a Docker environment to ensure consistent results across different systems.

### Using Dev Container (Recommended)

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Click the green button in the bottom-left corner and select "Reopen in Container"
4. Once inside the container:
   ```bash
   # Run with CSV file (default)
   uv run python -m duckdb_vs_polars_vs_fireducks

   # Or run with Parquet file (if you've created it)
   uv run python -m duckdb_vs_polars_vs_fireducks --file-type parquet
   ```

### Using Docker Compose

```bash
# Run with CSV file (default)
docker compose up

# Run with Parquet file
FILE_TYPE=parquet docker compose up
```

## Benchmark Types

1. **Simple Aggregation**: Basic aggregations (sum, mean, min, max) on a single column
2. **GroupBy Aggregation**: Same aggregations but grouped by VendorID and payment_type
3. **Self-Join**: Join the table with its own aggregation
4. **Window Function**: Dense rank calculation partitioned by payment_type

## Results

Results are saved as PNG files in the project directory, showing execution times for each operation across the different libraries.

## Libraries Compared

- **DuckDB**: A high-performance analytical database
- **Polars**: Fast DataFrame library written in Rust
- **Fireducks**: A fork of pandas optimized for performance

## Notes/Limitations

- Benchmarking DuckDB queries uses `.arrow()` to materialize results, as it was the fastest among `.arrow()`, `.pl()`, `.df()`, and `.fetchall()`.
- While `.execute()` could be used, it might not properly reflect full execution time as the final pipeline won't execute until a result collecting method is called.
- Polars uses `.collect()` to materialize results.
- Fireducks uses `._evaluate()` to ensure query execution.
- All libraries were tested with their default settings and no manual optimizations
- The goal was to compare "out of the box" performance with straightforward query implementations

For more details on DuckDB materialization, see [this Discord discussion](https://discord.com/channels/909674491309850675/921100786098901042/1217841718066413648).

## Future Plans for This Benchmark
Although, I don't have solid plans on how I want this repo to be, I plan on periodically run this benchmark as tools improve and get updates quickly. And potentially adding more queries to the benchmark down the road. 
