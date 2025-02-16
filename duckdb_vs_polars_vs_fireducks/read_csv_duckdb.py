import duckdb
from config import DATA_FILE_PATH_STR
def read_csv_duckdb(file_path):
    query = f'''
        select * from "{file_path}";
    '''
    return duckdb.sql(query).arrow()

if __name__ == '__main__':
    print(read_csv_duckdb(DATA_FILE_PATH_STR))