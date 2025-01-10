MODEL (
  name example.intermediate_model,
  owner Yuki,
  kind FULL,
  cron '@daily',
  grain id,
  column_descriptions (
    id = 'primary key',
    letter = 'alphabet letter',
    value = 'random value',
    updated_date = 'updated date',
    new_col = 'a new column'
  )
);

SELECT
  id,
  letter,
  value,
  @multiply_by_10(value) AS big_value,
  updated_date,
  'new_col' AS new_col
FROM example.base_model