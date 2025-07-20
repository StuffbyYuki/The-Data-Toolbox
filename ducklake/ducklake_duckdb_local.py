import duckdb 

def main():
    duckdb.sql("""
        INSTALL ducklake;
        LOAD ducklake;
        ATTACH 'ducklake:metadata.ducklake' AS my_ducklake (DATA_PATH 'ducklake_data_duckdb_local/');
        USE my_ducklake;
        CREATE or REPLACE TABLE my_table AS SELECT 1 AS my_number;
    """)
    print(
        duckdb.sql("SELECT * FROM my_table;"),
        duckdb.sql("SELECT * FROM ducklake_snapshots('my_ducklake');")
    )

if __name__ == "__main__":
    main()