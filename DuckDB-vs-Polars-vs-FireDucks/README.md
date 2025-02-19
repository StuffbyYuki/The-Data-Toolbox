# DuckDB vs Polars vs Fireducks Benchmark

A benchmark comparing DuckDB, Polars, and Fireducks for simple data operations.

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
tests/
├── __init__.py
└── test_output.py      # Tests for all query implementations
```

## Data
The benchmark uses the [NYC Yellow Taxi Trip Data](https://data.cityofnewyork.us/Transportation/2021-Yellow-Taxi-Trip-Data/m6nq-qud6/about_data) that contains 30M rows with 18 columns. 

Place your data file(s) in the `data` directory:
- Required: `data/2023_Yellow_Taxi_Trip_Data.csv` (3.78 GB)
- Optional: `data/2023_Yellow_Taxi_Trip_Data.parquet` (729 MB) - if you want to test Parquet format

## Libraries Compared

- **DuckDB**: A high-performance analytical database
- **Polars**: Fast DataFrame library written in Rust
- **Fireducks**: A faster, drop-in replacement for pandas

## Benchmark Queries

1. **Simple Aggregation**: Basic aggregations (sum, mean, min, max) on the `total_amount` column
2. **GroupBy Aggregation**: Aggregations (sum, mean, min, max) of `total_amount` grouped by `VendorID` and `payment_type`
3. **Self-Join**: Join the original table with aggregated `total_amount` sums (grouped by `VendorID`, `payment_type`, and pickup month)
4. **Window Functions**: Two window calculations:
   - Average `fare_amount` per `VendorID`
   - Dense rank of trips by `total_amount` within each `payment_type` partition

## Running the Benchmarks

- FireDucks requires the use of [Linux (manylinux) on the x86_64 architecture](https://fireducks-dev.github.io/docs/get-started/)
- Using docker is recommended as it ensures consistent results across different systems.

### Using Docker Compose

```bash
# Run with CSV file (default)
docker compose up

# Run with Parquet file
FILE_TYPE=parquet docker compose up

# Run tests
docker compose run app uv run pytest
```

You can adjust the container's resource allocation in the `docker-compose.yml` file:

```yaml
services:
  app:
    // ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '4'    # Limit to 4 CPU cores
          memory: 8G   # Limit to 8GB RAM
```

### Using Dev Container

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Click the button in the bottom-left corner and select "Reopen in Container"
4. Once inside the container:
   ```bash
   # Run with CSV file (default)
   uv run python duckdb_vs_polars_vs_fireducks

   # Or run with Parquet file (if you've created it)
   uv run python duckdb_vs_polars_vs_fireducks --file-type parquet

   # Run tests
   uv run pytest
   ```

## Results

Results show execution times in seconds for each operation across the different libraries.

### CSV Results
![CSV Benchmark Results](./output_csv.png)

### Parquet Results
![Parquet Benchmark Results](./output_parquet.png)

## Notes

- Benchmarking DuckDB queries uses `.arrow()` to materialize results, as it was the fastest among `.arrow()`, `.pl()`, `.df()`, and `.fetchall()`.
- While `.execute()` could be used, it might not properly reflect full execution time as the final pipeline won't execute until a result collecting method is called.
- Polars uses `.collect()` to materialize results.
- Fireducks uses `._evaluate()` to ensure query execution.
- All libraries were tested with their default settings and no manual optimizations
- The goal was to compare "out of the box" performance with straightforward query implementations

For more details on DuckDB materialization, see [this Discord discussion](https://discord.com/channels/909674491309850675/921100786098901042/1217841718066413648).
