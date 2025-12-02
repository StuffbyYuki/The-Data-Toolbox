import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator
from dotenv import load_dotenv

load_dotenv()


@dlt.source
def nyc_open_data_source():
    client = RESTClient(
        base_url="https://data.cityofnewyork.us/resource/",
        paginator=OffsetPaginator(
            limit=100_000,  # The maximum number of items to retrieve in each request.
            offset=0,  # The initial offset for the first request. Defaults to 0.
            offset_param="$offset",  # The name of the query parameter used to specify the offset. Defaults to "offset".
            limit_param="$limit",  # The name of the query parameter used to specify the limit. Defaults to "limit".
            total_path=None,  # A JSONPath expression for the total number of items. If not provided, pagination is controlled by maximum_offset and stop_after_empty_page.
            maximum_offset=1000,  # Optional maximum offset value. Limits pagination even without a total count.
            stop_after_empty_page=True,  # Whether pagination should stop when a page contains no result items. Defaults to True.
        ),
    )

    @dlt.resource(write_disposition="replace")
    def motor_vehicle_collisions():
        for page in client.paginate("h9gi-nx95"):
            yield page

    return [motor_vehicle_collisions]


def load_nyc_open_data_source():
    pipeline = dlt.pipeline(
        pipeline_name="nyc_open_data_pipeline",
        destination="ducklake",
        dataset_name="nyc_open_data",
        progress="log",
    )
    pipeline.run(
        nyc_open_data_source(),
        loader_file_format="parquet",
    )


if __name__ == "__main__":
    load_nyc_open_data_source()