import duckdb

print(duckdb.sql('select 1;'))

# read files
duckdb_relation = duckdb.sql('select * from read_parquet("data/sample_data.parquet")')
print(duckdb_relation)

# or
duckdb_relation = duckdb.read_parquet('data/sample_data.parquet')
print(duckdb_relation)

# write files
duckdb.sql('copy (select 1 as col_a) to "data/sample_data.csv" (format csv)')

# or
duckdb.sql('select 1 as col_a').write_parquet('data/sample_data.csv')

# working with s3 
# 'rel' as in duckdb relation
# read
duckdb.sql(f'''
    install httpfs;
    load httpfs;
    CREATE SECRET (
      TYPE S3,
      KEY_ID 'YOUR_KEY_ID',
      SECRET 'YOUR_SECRET',
      REGION 'YOUR_REGION'
    );
''')

rel = duckdb.sql('select * from read_parquet("s3://sandbox-data-lake/sample_data.parquet");')
print(rel)

# write 
rel.write_parquet("s3://sandbox-data-lake/sample_data.parquet")

# connect to a persistent database
con = duckdb.connect("~/my_db.db")
print(con.sql('show all tables;'))

# running duckdb sql on a polars dataframe
import polars as pl
df = pl.DataFrame({'a': [1,2,3]})
print(duckdb.sql('select * from df;'))