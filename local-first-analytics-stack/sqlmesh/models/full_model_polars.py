import typing as t
from datetime import datetime

import pandas as pd
import polars as pl
from sqlmesh import ExecutionContext, model
from sqlglot.expressions import to_column


@model(
    name="lakehouse.full_model_polars",
    kind="FULL",
    cron="@daily",
    grain=("crash_date", "zip_code", "contributing_factor", "vehicle_type"),
    partitioned_by="crash_date",
    clustered_by=("contributing_factor", "vehicle_type", "zip_code"),
    description="""
        - Full model for the NYC Open Data Motor Vehicle Collisions dataset. 
        - Aggregates over collisions by date, borough, contributing factor, and vehicle type.
    """,
    columns={
        "crash_date": "date",
        "zip_code": "text",
        "contributing_factor": "text",
        "vehicle_type": "text",
        "collision_count": "bigint",
        "total_number_of_persons_injured": "bigint",
        "total_number_of_persons_killed": "bigint",
        "_lakehouse_loaded_at": "timestamp",
    },
    column_descriptions={
        "crash_date": "Occurrence date of collision",
        "zip_code": "Postal code of incident occurrence",
        "collision_count": "Total number of collisions",
        "total_number_of_persons_injured": "Total number of persons injured",
        "total_number_of_persons_killed": "Total number of persons killed",
        "contributing_factor": "Factors contributing to the collision for designated vehicle",
        "vehicle_type": "Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)",
        "_lakehouse_loaded_at": "Timestamp of when the record was loaded into the lakehouse",
    },
    audits=[
        ("unique_combination_of_columns", {"columns": [to_column("crash_date"), to_column("zip_code"), to_column("contributing_factor"), to_column("vehicle_type")]}),
        ("not_null", {"columns": [to_column("crash_date")]})
    ],
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: t.Any,
) -> pd.DataFrame:
    """
    Python (Polars) version of `lakehouse.full_model`.

    Reads from `lakehouse.incremental_model`, aggregates, and returns a Pandas DataFrame.
    """
    source = context.resolve_table("lakehouse.incremental_model")

    pandas_df = context.fetchdf(
        f"""
        SELECT
          crash_date,
          zip_code,
          contributing_factor_vehicle_1,
          vehicle_type_code1,
          number_of_persons_injured,
          number_of_persons_killed
        FROM {source}
        """
    ) 

    df = (
        pl.from_pandas(pandas_df)
        .group_by(
            ["crash_date", "zip_code", "contributing_factor_vehicle_1", "vehicle_type_code1"],
            maintain_order=False,
        )
        .agg(
            pl.len().alias("collision_count"),
            pl.col("number_of_persons_injured").sum().alias("total_number_of_persons_injured"),
            pl.col("number_of_persons_killed").sum().alias("total_number_of_persons_killed"),
        )
        .rename(
            {
                "contributing_factor_vehicle_1": "contributing_factor",
                "vehicle_type_code1": "vehicle_type",
            }
        )
        .with_columns(pl.lit(execution_time).alias("_lakehouse_loaded_at"))
        .select(
            [
                "crash_date",
                "zip_code",
                "contributing_factor",
                "vehicle_type",
                "collision_count",
                "total_number_of_persons_injured",
                "total_number_of_persons_killed",
                "_lakehouse_loaded_at",
            ]
        )
    )

    return df.to_pandas()


