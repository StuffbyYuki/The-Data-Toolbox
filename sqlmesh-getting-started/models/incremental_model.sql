MODEL (
    name example.incremental_model,
    owner Yuki,
    kind INCREMENTAL_BY_TIME_RANGE (
        time_column (updated_date, '%Y-%m-%d'),
        lookback 5,  -- to handle late arriving date
    ),
    start '2025-01-01',
    cron '@daily',
    grain id,
    column_descriptions (
        id = 'primary key',
        letter = 'alphabet letter',
        updated_date = 'updated date',
    )
  );

  SELECT
    id,
    letter,
    updated_date
  FROM
    example.base_model
  WHERE 
    updated_date BETWEEN @start_date AND @end_date
  