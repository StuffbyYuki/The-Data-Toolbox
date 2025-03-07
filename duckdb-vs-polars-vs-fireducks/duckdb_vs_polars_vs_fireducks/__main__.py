import importlib
import pathlib
import timeit
import argparse
import gc
from visualize_output import visualize_output
from config import get_data_file_path_str


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Run benchmarks on CSV or Parquet files."
    )
    parser.add_argument(
        "--file-type",
        choices=["csv", "parquet"],
        default="csv",
        help="File type to use for benchmarks (default: parquet)",
    )

    args = parser.parse_args()
    file_path = get_data_file_path_str(args.file_type)

    outputs = []
    queries_dir = pathlib.Path(__file__).parent / "queries"

    matches = [
        f
        for pattern in ["*duckdb.py", "*fireducks.py", "*polars.py"]
        for f in queries_dir.glob(pattern)
    ]

    for benchmark in sorted(matches):
        module_name = f"queries.{benchmark.with_suffix('').name}"
        module = importlib.import_module(module_name)
        benchmark_function = getattr(module, benchmark.with_suffix("").name)
        query_type = "_".join(benchmark.stem.split("_")[:-1])
        library = benchmark.stem.split("_")[-1]

        # Use timeit to measure the average execution time
        total_time = timeit.repeat(
            stmt=lambda: benchmark_function(file_path),
            repeat=3,
            number=1
        )
        average_time = round(sum(total_time) / len(total_time), 2)
        print(benchmark.stem, average_time)

        output = [average_time, query_type, library]
        outputs.append(output)

    visualize_output(outputs, args.file_type)

if __name__ == "__main__":
    main()
