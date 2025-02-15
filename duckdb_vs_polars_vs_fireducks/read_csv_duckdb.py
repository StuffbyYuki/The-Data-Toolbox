import duckdb

def read_csv_duckdb(file_path):
    query = f'''
        select * from "{file_path}";
    '''
    return duckdb.sql(query).arrow()

if __name__ == '__main__':
    print(read_csv_duckdb('data/2021_Yellow_Taxi_Trip_Data.csv'))