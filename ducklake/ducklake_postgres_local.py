import duckdb
import os
import dotenv

dotenv.load_dotenv(override=True)


def main():
    host = os.getenv('LOCAL_HOST', 'localhost')
    port = os.getenv('LOCAL_PORT', '5432')
    user = os.getenv('LOCAL_USER', 'ducklake_user')
    password = os.getenv('LOCAL_PASSWORD', 'ducklake_password')
    dbname = os.getenv('LOCAL_DBNAME', 'ducklake_catalog')
    
    duckdb.sql(f"""
        INSTALL ducklake;
        LOAD ducklake;
        INSTALL postgres;
        LOAD postgres;
        ATTACH 'ducklake:postgres:dbname={dbname} host={host} port={port} user={user} password={password}' AS my_ducklake (DATA_PATH 'ducklake_data_postgres_local/');
        USE my_ducklake;
        CREATE or REPLACE TABLE my_table AS SELECT 2 AS my_number;
    """)
    print(
        duckdb.sql("SELECT * FROM my_table;"),
        duckdb.sql("SELECT * FROM ducklake_snapshots('my_ducklake');")
    )

if __name__ == "__main__":
    main() 