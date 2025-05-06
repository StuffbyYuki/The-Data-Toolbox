import bauplan
from bauplan.standard_expectations import (
    expect_column_no_nulls,
    expect_column_all_unique,
)


# stg_customers
@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_customers_customer_id_no_nulls(data=bauplan.Model("stg_customers")):
    column_to_check = "customer_id"
    _is_expectation_correct = expect_column_no_nulls(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have no null values"
    )

    return _is_expectation_correct  # return a boolean


@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_customers_customer_id_unique(data=bauplan.Model("stg_customers")):
    column_to_check = "customer_id"
    _is_expectation_correct = expect_column_all_unique(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have all unique values"
    )

    return _is_expectation_correct  # return a boolean


# stg_products
@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_products_product_id_no_nulls(data=bauplan.Model("stg_products")):
    column_to_check = "product_id"
    _is_expectation_correct = expect_column_no_nulls(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have no null values"
    )

    return _is_expectation_correct


@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_products_product_id_unique(data=bauplan.Model("stg_products")):
    column_to_check = "product_id"
    _is_expectation_correct = expect_column_all_unique(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have all unique values"
    )

    return _is_expectation_correct


# stg_orders
@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_orders_order_id_no_nulls(data=bauplan.Model("stg_orders")):
    column_to_check = "order_id"
    _is_expectation_correct = expect_column_no_nulls(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have no null values"
    )

    return _is_expectation_correct


@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_orders_order_id_unique(data=bauplan.Model("stg_orders")):
    column_to_check = "order_id"
    _is_expectation_correct = expect_column_all_unique(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have all unique values"
    )

    return _is_expectation_correct


# stg_order_items
@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_order_items_order_item_id_no_nulls(data=bauplan.Model("stg_order_items")):
    column_to_check = "order_item_id"
    _is_expectation_correct = expect_column_no_nulls(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have no null values"
    )

    return _is_expectation_correct


@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_order_items_order_item_id_unique(data=bauplan.Model("stg_order_items")):
    column_to_check = "order_item_id"
    _is_expectation_correct = expect_column_all_unique(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have all unique values"
    )

    return _is_expectation_correct


# stg_supplies
@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_supplies_supply_id_no_nulls(data=bauplan.Model("stg_supplies")):
    column_to_check = "supply_id"
    _is_expectation_correct = expect_column_no_nulls(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have no null values"
    )

    return _is_expectation_correct


@bauplan.expectation()
@bauplan.python("3.11")
def check_stg_supplies_supply_uuid_unique(data=bauplan.Model("stg_supplies")):
    column_to_check = "supply_uuid"
    _is_expectation_correct = expect_column_all_unique(data, column_to_check)

    assert _is_expectation_correct, (
        f"expectation test failed: we expected {column_to_check} to have all unique values"
    )

    return _is_expectation_correct
