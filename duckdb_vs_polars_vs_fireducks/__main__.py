import importlib
import pathlib
import time
import argparse
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
        default="parquet",
        help="File type to use for benchmarks (default: parquet)",
    )

    args = parser.parse_args()

    # Get file path based on argument
    file_path = get_data_file_path_str(args.file_type)

    outputs = []
    this_dir = pathlib.Path(__file__).parent

    matches = [
        f
        for pattern in ["*duckdb.py", "*fireducks.py", "*polars.py"]
        for f in this_dir.glob(pattern)
    ]

    for benchmark in sorted(matches):
        module_name = func_name = benchmark.with_suffix("").name
        module = importlib.import_module(module_name)
        benchmark_function = getattr(module, func_name)
        query_type = "_".join(func_name.split("_")[:-1])
        library = func_name.split("_")[-1]

        start = time.time()
        benchmark_function(file_path)
        end = time.time()
        seconds = round(end - start, 2)
        print(func_name, seconds)

        output = [seconds, query_type, library]
        outputs.append(output)

    # Pass file type to visualize_output for naming the output file
    visualize_output(outputs, args.file_type)


if __name__ == "__main__":
    main()
