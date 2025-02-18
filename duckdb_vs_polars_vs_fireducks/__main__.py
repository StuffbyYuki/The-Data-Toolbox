import importlib
import pathlib
import time
from visualize_output import visualize_output
from config import DATA_FILE_PATH_STR


def main():
    outputs = []
    this_dir = pathlib.Path(__file__).parent

    for benchmark in sorted(this_dir.glob("*[duckdb|fireducks|pandas|polars].py")):
        module_name = func_name = benchmark.with_suffix("").name
        module = importlib.import_module(module_name)
        benchmark_function = getattr(module, func_name)
        query_type = "_".join(func_name.split("_")[:-1])
        library = func_name.split("_")[-1]

        start = time.time()
        benchmark_function(DATA_FILE_PATH_STR)
        end = time.time()
        seconds = round(end - start, 2)
        print(func_name, seconds)

        output = [seconds, query_type, library]
        outputs.append(output)

    visualize_output(outputs)


if __name__ == "__main__":
    main()
