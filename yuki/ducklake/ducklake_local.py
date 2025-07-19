import duckdb
import os


def setup_ducklake(attach_statement):
    con = duckdb.connect()
    
    # Install required extensions
    extensions = ["ducklake"]
    if 'postgres' in attach_statement:
        extensions.append("postgres")
    
    for ext in extensions:
        con.sql(f"INSTALL {ext}; LOAD {ext};")
    
    # Attach and use ducklake
    con.sql(f"{attach_statement}; USE my_ducklake;")
    
    # Create test table and show results
    con.sql("CREATE OR REPLACE TABLE my_table AS SELECT 1 AS my_number;")
    
    print("----- Show table contents -----")
    print(con.sql("SELECT * FROM my_table;"))
    print("----- Show snapshot -----")
    print(con.sql("SELECT * FROM ducklake_snapshots('my_ducklake');"))


def main():
    # DuckDB metastore
    print("=== DuckDB Metastore ===\n")
    setup_ducklake(
        "ATTACH 'ducklake:metadata.ducklake' AS my_ducklake (DATA_PATH 'data_files_duckdb_metastore')"
    )
    
    # PostgreSQL metastore - use environment variables for container connection
    print("\n=== PostgreSQL Metastore ===\n")
    host = os.getenv('HOST', 'localhost')
    port = os.getenv('PORT', '5432')
    user = os.getenv('USER', 'ducklake_user')
    password = os.getenv('PASSWORD', 'ducklake_password')
    dbname = os.getenv('DBNAME', 'ducklake_catalog')
    
    setup_ducklake(
        f"ATTACH 'ducklake:postgres:dbname={dbname} host={host} port={port} "
        f"user={user} password={password}' AS my_ducklake "
        f"(DATA_PATH 'data_files_postgres_metastore/')"
    )


if __name__ == "__main__":
    main()

