MODEL (
  name example.base_model,
  owner Yuki,
  kind VIEW,
  cron '@daily',
  grain id,
  column_descriptions (
    id = 'primary key',
    letter = 'alphabet letter',
    value = 'random value',
    updated_date = 'updated date'
  ),
  audits (assert_positive_ids, UNIQUE_VALUES(columns = id), NOT_NULL(columns = id))
);

SELECT
  id::INT,
  letter::TEXT,
  value::INT,
  updated_date::DATE
FROM example.letters