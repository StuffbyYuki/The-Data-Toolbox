import typing as t
from datetime import datetime

from sqlmesh import ExecutionContext, model
import pandas as pd
import polars as pl

@model(
    name='example.intermediate_py_model',
    owner='Yuki',
    kind='FULL',
    cron='@daily',
    grain='id',
    columns={
        'id': 'int',
        'letter': 'text',
        'value': 'int',
        'big_value': 'int',
        'updated_date': 'date',
        'new_col': 'text'
    },
    column_descriptions={
        'id': 'primary key',
        'letter': 'alphabet letter',
        'value': 'random value',
        'big_value': 'value * 10',
        'updated_date': 'updated date',
        'new_col': 'a new column'
    }
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: t.Any,
):

    table = context.resolve_table("example.base_model")
    df = (
        pl.from_pandas(context.fetchdf(f"SELECT * FROM {table}"))
        .select(
            'id',
            'letter',
            'value',
            pl.col('value').mul(10).alias('big_value'),
            'updated_date',
            pl.lit('new_col').alias('new_col')
        )
    )

    return df.to_pandas()