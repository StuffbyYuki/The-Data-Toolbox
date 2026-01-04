MODEL (
  name lakehouse.incremental_model,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column crash_date
  ),
  cron '@daily',  -- this model runs daily at 00:00 UTC
  grain (collision_id),
  columns (
    collision_id BIGINT,
    crash_date TIMESTAMPTZ,
    crash_time TIME,
    borough TEXT,
    zip_code TEXT,
    number_of_persons_injured INTEGER,
    number_of_persons_killed INTEGER,
    _lakehouse_loaded_at TIMESTAMP
  ),
  audits (
    unique_values(columns = collision_id),
    not_null(columns = collision_id)
  )
);

SELECT
  -- Primary key / grain
  collision_id,
  -- Time
  crash_date,
  crash_time,
  -- Location
  borough,
  zip_code,
  -- Impact counts
  number_of_persons_injured,
  number_of_persons_killed,
  -- lakehouse metadata
  CURRENT_TIMESTAMP() AS _lakehouse_loaded_at,

FROM lakehouse.base_model
WHERE crash_date BETWEEN @start_date AND @end_date;
