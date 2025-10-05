MODEL (
  name sqlmesh_example.full_model,
  kind FULL,
  cron '@daily',
  grain item_id,
  audits (assert_positive_order_ids),
);

SELECT
  item_id,
  COUNT(DISTINCT id) * 2 AS num_orders,
  1 as new_col_one
FROM
  sqlmesh_example.incremental_model
GROUP BY item_id
  