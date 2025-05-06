import bauplan
import duckdb


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def order_items(
    stg_order_items=bauplan.Model("yuki.stg_order_items"),
    stg_orders=bauplan.Model("yuki.stg_orders"),
    stg_products=bauplan.Model("yuki.stg_products"),
    stg_supplies=bauplan.Model("yuki.stg_supplies"),
):
    """
    name: order_items
    description: Order item-level metrics and attributes
    """
    sql = """
    WITH order_supplies_summary AS (
        SELECT
            product_id,
            SUM(supply_cost) as supply_cost
        FROM stg_supplies
        GROUP BY 1
    )
    SELECT
        stg_order_items.*,
        stg_orders.ordered_at,
        stg_products.product_name,
        stg_products.product_price,
        stg_products.is_food_item,
        stg_products.is_drink_item,
        order_supplies_summary.supply_cost
    FROM stg_order_items
    LEFT JOIN stg_orders
        ON stg_order_items.order_id = stg_orders.order_id
    LEFT JOIN stg_products
        ON stg_order_items.product_id = stg_products.product_id
    LEFT JOIN order_supplies_summary
        ON stg_order_items.product_id = order_supplies_summary.product_id
    """
    return duckdb.sql(sql).arrow()


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def orders(
    stg_orders=bauplan.Model("yuki.stg_orders"),
    order_items=bauplan.Model("yuki.order_items"),
):
    """
    name: orders
    description: Order-level metrics and attributes
    """
    sql = """
    WITH order_items_summary AS (
        SELECT
            order_id,
            SUM(supply_cost) as order_cost,
            SUM(product_price) as order_items_subtotal,
            COUNT(order_item_id) as count_order_items,
            SUM(CASE WHEN is_food_item THEN 1 ELSE 0 END) as count_food_items,
            SUM(CASE WHEN is_drink_item THEN 1 ELSE 0 END) as count_drink_items
        FROM order_items
        GROUP BY 1
    ),
    compute_booleans AS (
        SELECT
            stg_orders.*,
            order_items_summary.order_cost,
            order_items_summary.order_items_subtotal,
            order_items_summary.count_food_items,
            order_items_summary.count_drink_items,
            order_items_summary.count_order_items,
            order_items_summary.count_food_items > 0 as is_food_order,
            order_items_summary.count_drink_items > 0 as is_drink_order
        FROM stg_orders
        LEFT JOIN order_items_summary
            ON stg_orders.order_id = order_items_summary.order_id
    )
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY ordered_at ASC
        ) as customer_order_number
    FROM compute_booleans
    """
    return duckdb.sql(sql).arrow()


@bauplan.model(materialization_strategy="REPLACE")
@bauplan.python("3.11", pip={"duckdb": "1.2.2"})
def customers(
    stg_customers=bauplan.Model("yuki.stg_customers"),
    orders=bauplan.Model("yuki.orders"),
):
    """
    name: customers
    description: Customer-level metrics and attributes
    """
    sql = """
    WITH customer_orders_summary AS (
        SELECT
            orders.customer_id,
            COUNT(DISTINCT orders.order_id) as count_lifetime_orders,
            COUNT(DISTINCT orders.order_id) > 1 as is_repeat_buyer,
            MIN(orders.ordered_at) as first_ordered_at,
            MAX(orders.ordered_at) as last_ordered_at,
            SUM(orders.subtotal) as lifetime_spend_pretax,
            SUM(orders.tax_paid) as lifetime_tax_paid,
            SUM(orders.order_total) as lifetime_spend
        FROM orders
        GROUP BY 1
    )
    SELECT
        stg_customers.*,
        customer_orders_summary.count_lifetime_orders,
        customer_orders_summary.first_ordered_at,
        customer_orders_summary.last_ordered_at,
        customer_orders_summary.lifetime_spend_pretax,
        customer_orders_summary.lifetime_tax_paid,
        customer_orders_summary.lifetime_spend,
        CASE
            WHEN customer_orders_summary.is_repeat_buyer THEN 'returning'
            ELSE 'new'
        END as customer_type
    FROM stg_customers
    LEFT JOIN customer_orders_summary
        ON stg_customers.customer_id = customer_orders_summary.customer_id
    """
    return duckdb.sql(sql).arrow()
