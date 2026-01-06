MODEL (
  name lakehouse.full_model,
  kind FULL, 
  cron '@daily',  -- this model runs daily at 00:00 UTC
  grain (crash_date, zipcode, contributing_factor, vehicle_type),
  partitioned_by crash_date,
  clustered_by (contributing_factor, vehicle_type, zip_code),
  description """
    - Full model for the NYC Open Data Motor Vehicle Collisions dataset. 
    - Aggregates over collisions by date, borough, contributing factor, and vehicle type.
  """,
  column_descriptions (
    crash_date = 'Occurrence date of collision',
    zip_code = 'Postal code of incident occurrence',
    total_number_of_persons_injured = 'Total number of persons injured',
    total_number_of_persons_killed = 'Total number of persons killed',
    contributing_factor = 'Factors contributing to the collision for designated vehicle',
    vehicle_type = 'Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)',
    _lakehouse_loaded_at = 'Timestamp of when the record was loaded into the lakehouse',
  ),
  audits (
    unique_combination_of_columns(columns = (crash_date, zip_code, contributing_factor, vehicle_type)),
    not_null(columns = (crash_date))
  )
);

SELECT
  crash_date,
  zip_code,
  contributing_factor_vehicle_1 as contributing_factor, 
  vehicle_type_code1 as vehicle_type,
  SUM(number_of_persons_injured) as total_number_of_persons_injured,
  SUM(number_of_persons_killed) as total_number_of_persons_killed,
  CURRENT_TIMESTAMP() AS _lakehouse_loaded_at

FROM lakehouse.incremental_model
GROUP BY
  crash_date,
  zip_code,
  contributing_factor_vehicle_1, 
  vehicle_type_code1
