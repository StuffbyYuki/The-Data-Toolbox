import duckdb
import os
import dotenv

dotenv.load_dotenv(override=True)

def main():
    
    duckdb.sql(f"""
        INSTALL ducklake;
        LOAD ducklake;
        INSTALL postgres;
        LOAD postgres;
        CREATE SECRET (
            TYPE r2,
            KEY_ID '{os.getenv('R2_ACCESS_KEY_ID')}',
            SECRET '{os.getenv('R2_SECRET_ACCESS_KEY')}',
            ACCOUNT_ID '{os.getenv('R2_ACCOUNT_ID')}'
        );
        ATTACH 'ducklake:postgres:dbname={os.getenv('DBNAME')} host={os.getenv('HOST')} port={os.getenv('PORT')} user={os.getenv('USER')} password={os.getenv('PASSWORD')} sslmode=require' AS my_ducklake (DATA_PATH 'r2://{os.getenv('R2_BUCKET_NAME')}/ducklake/');
        USE my_ducklake;
        CREATE or REPLACE TABLE my_table AS SELECT 3 AS my_number;
    """)
    print(
        duckdb.sql(f"SELECT * FROM my_table;"),
        duckdb.sql("SELECT * FROM ducklake_snapshots('my_ducklake');")
    )

if __name__ == "__main__":
    main()

