MODEL (
  name lakehouse.base_model,
  kind full,
  cron '@daily',
  grain (collision_id),
  columns (
    crash_date TIMESTAMPTZ,
    crash_time TEXT,
    on_street_name TEXT,
    off_street_name TEXT,
    number_of_persons_injured TEXT,
    number_of_persons_killed TEXT,
    number_of_pedestrians_injured TEXT,
    number_of_pedestrians_killed TEXT,
    number_of_cyclist_injured TEXT,
    number_of_cyclist_killed TEXT,
    number_of_motorist_injured TEXT,
    number_of_motorist_killed TEXT,
    contributing_factor_vehicle_1 TEXT,
    contributing_factor_vehicle_2 TEXT,
    collision_id TEXT,
    vehicle_type_code1 TEXT,
    vehicle_type_code2 TEXT,
    _dlt_load_id TEXT,
    _dlt_id TEXT,
    borough TEXT,
    zip_code TEXT,
    latitude TEXT,
    longitude TEXT,
    location__latitude TEXT,
    location__longitude TEXT,
    location__human_address TEXT,
    contributing_factor_vehicle_3 TEXT,
    vehicle_type_code_3 TEXT,
    cross_street_name TEXT,
    contributing_factor_vehicle_4 TEXT,
    vehicle_type_code_4 TEXT,
    contributing_factor_vehicle_5 TEXT,
    vehicle_type_code_5 TEXT,
  ),
  audits (
    unique_values(columns = collision_id),
    not_null(columns = collision_id)
  )
);

SELECT
  -- Primary key / grain
  collision_id,
  -- Event time
  crash_date,
  crash_time,
  -- Location (street context)
  on_street_name,
  off_street_name,
  cross_street_name,
  -- Location (geo)
  borough,
  zip_code,
  latitude,
  longitude,
  location__latitude,
  location__longitude,
  location__human_address,
  -- Impact counts
  number_of_persons_injured,
  number_of_persons_killed,
  number_of_pedestrians_injured,
  number_of_pedestrians_killed,
  number_of_cyclist_injured,
  number_of_cyclist_killed,
  number_of_motorist_injured,
  number_of_motorist_killed,
  -- Contributing factors
  contributing_factor_vehicle_1,
  contributing_factor_vehicle_2,
  contributing_factor_vehicle_3,
  contributing_factor_vehicle_4,
  contributing_factor_vehicle_5,
  -- Vehicle type codes
  vehicle_type_code1,
  vehicle_type_code2,
  vehicle_type_code_3,
  vehicle_type_code_4,
  vehicle_type_code_5,
  -- dlt metadata
  _dlt_load_id,
  _dlt_id

FROM nyc_open_data.motor_vehicle_collisions;
