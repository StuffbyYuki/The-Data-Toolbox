import duckdb

def groupby_agg_duckdb(file_path):
    query = f'''
        select 
            VendorID,
            payment_type,
            sum(total_amount),
            avg(total_amount),
            min(total_amount),
            max(total_amount)
        from "{file_path}"
        group by
            VendorID,
            payment_type
        ;
    '''
    return duckdb.sql(query).arrow()

if __name__ == '__main__':
    print(groupby_agg_duckdb('data/2021_Yellow_Taxi_Trip_Data.csv'))