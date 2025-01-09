AUDIT (
    name assert_positive_ids,
  );

  SELECT *
  FROM @this_model
  WHERE
    id < 0
  