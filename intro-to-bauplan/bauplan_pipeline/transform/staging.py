import bauplan
import duckdb
from utils import cents_to_dollars
from duckdb.typing import FLOAT, BIGINT

duckdb.create_function("cents_to_dollars", cents_to_dollars, [BIGINT], FLOAT)


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def stg_customers(
    raw_customers=bauplan.Model(
        "yuki.raw_customers",
        columns=["id", "name"],
    ),
):
    """
    name:
    description:
    columns:
        - customer_id: The unique key for each customer.
        - customer_name: The name of each customer
    """
    sql = """
    SELECT
        id AS customer_id, 
        name AS customer_name
    FROM raw_customers
    """

    return duckdb.sql(sql).arrow()


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def stg_order_items(
    raw_items=bauplan.Model(
        "yuki.raw_items",
        columns=["id", "order_id", "sku"],
    ),
):
    """
    name:
    description:
    """
    sql = """
    SELECT
        id AS order_item_id,
        order_id,
        sku AS product_id
    FROM raw_items
    """

    return duckdb.sql(sql).arrow()


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def stg_orders(
    raw_orders=bauplan.Model(
        "yuki.raw_orders",
        columns=[
            "id",
            "store_id",
            "customer",
            "subtotal",
            "tax_paid",
            "order_total",
            "ordered_at",
        ],
    ),
):
    """
    name:
    description:
    """
    sql = """
    SELECT
        id AS order_id,
        store_id AS location_id,
        customer AS customer_id,
        subtotal AS subtotal_cents,
        tax_paid AS tax_paid_cents,
        order_total AS order_total_cents,
        cents_to_dollars(subtotal) AS subtotal,
        cents_to_dollars(tax_paid) AS tax_paid,
        cents_to_dollars(order_total) AS order_total,
        date_trunc('day', ordered_at) AS ordered_at
    FROM raw_orders
    """

    return duckdb.sql(sql).arrow()


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def stg_products(
    raw_products=bauplan.Model(
        "yuki.raw_products",
        columns=["sku", "name", "description", "price", "type"],
    ),
):
    """
    name:
    description:
    columns:
        - product_id: The unique key for each product.
        - product_name: The name of each product
        - product_description: The description of each product
        - product_price: The price of each product
    """
    sql = """
    SELECT
        sku AS product_id, 
        name AS product_name,
        description AS product_description,
        cents_to_dollars(price) AS product_price,
        coalesce("type" = 'jaffle', false) AS is_food_item,
        coalesce("type" = 'beverage', false) AS is_drink_item
    FROM raw_products
    """

    return duckdb.sql(sql).arrow()


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def stg_supplies(
    raw_supplies=bauplan.Model(
        "yuki.raw_supplies",
        columns=["id", "sku", "name", "cost", "perishable"],
    ),
):
    """
    name:
    description:
    columns:
        - supplier_id: The unique key for each supplier.
        - supplier_name: The name of each supplier
        - supplier_cost: The cost of each supplier
        - is_perishable_supply: Whether the supplier is perishable
    """
    sql = """
    SELECT
        id AS supply_id, 
        sku AS product_id,
        name AS supply_name,
        cents_to_dollars(cost) AS supply_cost,
        perishable AS is_perishable_supply
    FROM raw_supplies
    """

    return duckdb.sql(sql).arrow()
