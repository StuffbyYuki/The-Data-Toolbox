import bauplan


def create_and_import_table(table_name, search_uri, branch_name, namespace):
    client = bauplan.Client()

    # Create the table
    client.create_table(
        table=table_name, search_uri=search_uri, branch=branch_name, namespace=namespace
    )

    # Import the data
    state = client.import_data(
        table=table_name, search_uri=search_uri, branch=branch_name, namespace=namespace
    )

    # Check for errors during import
    if state.error:
        print(f"Import failed: {state.error}")


if __name__ == "__main__":
    tables = [
        "raw_customers",
        "raw_items",
        "raw_orders",
        "raw_products",
        "raw_supplies",
    ]
    namespace = "yuki"
    branch_name = "yuki.sandbox"
    search_uri = "s3://alpha-hello-bauplan/yuki/{table}.csv"

    for table in tables:
        print(f"Creating and importing table: {table}")
        try:
            create_and_import_table(
                table_name=table,
                search_uri=search_uri.format(table=table),
                branch_name=branch_name,
                namespace=namespace,
            )
        except Exception as e:
            print(f"Error creating and importing table: {e}")
            print(f"Error message: {e}")
