import duckdb
import os
import dotenv

dotenv.load_dotenv(override=True)

def setup_ducklake(attach_statement):
    con = duckdb.connect()
    
    # Install required extensions
    extensions = ["ducklake"]
    if 'postgres' in attach_statement:
        extensions.append("postgres")
    
    for ext in extensions:
        con.sql(f"INSTALL {ext}; LOAD {ext};")

    # Create R2 secret
    con.sql(f"""
        CREATE SECRET (
            TYPE r2,
            KEY_ID '{os.getenv('R2_ACCESS_KEY_ID')}',
            SECRET '{os.getenv('R2_SECRET_ACCESS_KEY')}',
            ACCOUNT_ID '{os.getenv('R2_ACCOUNT_ID')}'
        );
    """)

    # Attach and use ducklake
    con.sql(f"{attach_statement}; USE my_ducklake;")
    
    # Test write and read
    bucket_path = f"r2://{os.getenv('R2_BUCKET_NAME')}/my_table.parquet"
    con.sql(f"COPY (SELECT 1) TO '{bucket_path}'")
    
    print("----- Show table contents -----")
    print(con.sql(f"SELECT * FROM read_parquet('{bucket_path}');"))
    print("----- Show snapshot -----")
    print(con.sql("SELECT * FROM ducklake_snapshots('my_ducklake');"))


def main():
    print("\n=== PostgreSQL Metastore ===\n")
    
    attach_stmt = (
        f"ATTACH 'ducklake:postgres:dbname={os.getenv('DBNAME')} "
        f"host={os.getenv('HOST')} port={os.getenv('PORT')} "
        f"user={os.getenv('USER')} password={os.getenv('PASSWORD')} "
        f"sslmode=require' AS my_ducklake (DATA_PATH 'data_files_postgres_metastore/')"
    )
    
    setup_ducklake(attach_stmt)


if __name__ == "__main__":
    main()

