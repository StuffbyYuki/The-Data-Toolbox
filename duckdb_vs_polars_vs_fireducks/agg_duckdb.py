import duckdb
from config import DATA_FILE_PATH_STR


def agg_duckdb(file_path):
    query = f'''
        select 
            sum(total_amount),
            avg(total_amount),
            min(total_amount),
            max(total_amount)
        from "{file_path}"
        ;
    '''
    return duckdb.sql(query).arrow()

if __name__ == '__main__':
    print(agg_duckdb(DATA_FILE_PATH_STR))