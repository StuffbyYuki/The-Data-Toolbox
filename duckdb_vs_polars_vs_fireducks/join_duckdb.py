import duckdb

def join_duckdb(file_path):
    query = f'''

        with base as (
            select 
                *,
                month(tpep_pickup_datetime) pickup_month,
            from "{file_path}"
        ),
        
        join_data as (
            select 
                VendorID,
                payment_type,
                pickup_month,
                sum(total_amount)
            from base
            group by
                VendorID,
                payment_type,
                pickup_month
        )
            
        select *
        from base
        inner join join_data
            using (VendorID, payment_type, pickup_month) 
        ;
    '''
    return duckdb.sql(query).arrow()

if __name__ == '__main__':
    print(join_duckdb('data/2021_Yellow_Taxi_Trip_Data.csv'))