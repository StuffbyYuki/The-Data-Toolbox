MODEL (
  name lakehouse.base_model,
  kind full,
  cron '@daily',
  grain (collision_id),
  columns (
    collision_id BIGINT,
    crash_date TIMESTAMPTZ,
    crash_time TIME,
    on_street_name TEXT,
    off_street_name TEXT,
    cross_street_name TEXT,
    borough TEXT,
    zip_code TEXT,
    latitude DOUBLE,
    longitude DOUBLE,
    location__latitude DOUBLE,
    location__longitude DOUBLE,
    location__human_address TEXT,
    number_of_persons_injured INTEGER,
    number_of_persons_killed INTEGER,
    number_of_pedestrians_injured INTEGER,
    number_of_pedestrians_killed INTEGER,
    number_of_cyclist_injured INTEGER,
    number_of_cyclist_killed INTEGER,
    number_of_motorist_injured INTEGER,
    number_of_motorist_killed INTEGER,
    contributing_factor_vehicle_1 TEXT,
    contributing_factor_vehicle_2 TEXT,
    contributing_factor_vehicle_3 TEXT,
    contributing_factor_vehicle_4 TEXT,
    contributing_factor_vehicle_5 TEXT,
    vehicle_type_code1 TEXT,
    vehicle_type_code2 TEXT,
    vehicle_type_code_3 TEXT,
    vehicle_type_code_4 TEXT,
    vehicle_type_code_5 TEXT,
    _dlt_load_id BIGINT,
    _dlt_id TEXT,
  ),
  audits (
    unique_values(columns = collision_id),
    not_null(columns = collision_id)
  )
);

SELECT
  -- Primary key / grain
  collision_id::BIGINT,
  -- Event time
  crash_date::TIMESTAMPTZ,
  crash_time::TIME,
  -- Location (street context)
  on_street_name::TEXT,
  off_street_name::TEXT,
  cross_street_name::TEXT,
  -- Location (geo)
  borough::TEXT,
  zip_code::TEXT,
  latitude::DOUBLE,
  longitude::DOUBLE,
  location__latitude::DOUBLE,
  location__longitude::DOUBLE,
  location__human_address::TEXT,
  -- Impact counts
  number_of_persons_injured::INTEGER,
  number_of_persons_killed::INTEGER,
  number_of_pedestrians_injured::INTEGER,
  number_of_pedestrians_killed::INTEGER,
  number_of_cyclist_injured::INTEGER,
  number_of_cyclist_killed::INTEGER,
  number_of_motorist_injured::INTEGER,
  number_of_motorist_killed::INTEGER,
  -- Contributing factors
  contributing_factor_vehicle_1::TEXT,
  contributing_factor_vehicle_2::TEXT,
  contributing_factor_vehicle_3::TEXT,
  contributing_factor_vehicle_4::TEXT,
  contributing_factor_vehicle_5::TEXT,
  -- Vehicle type codes
  vehicle_type_code1::TEXT,
  vehicle_type_code2::TEXT,
  vehicle_type_code_3::TEXT,
  vehicle_type_code_4::TEXT,
  vehicle_type_code_5::TEXT,
  -- dlt metadata
  _dlt_load_id::BIGINT,
  _dlt_id::TEXT

FROM nyc_open_data.motor_vehicle_collisions;
