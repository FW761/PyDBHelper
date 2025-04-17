from db import py_db_helper
from dataclasses import dataclass
from factory_connect import fact_conn


def main():

    fc = fact_conn.FactoryConnect()
    conn = [{'driver_name': 'postgresql', 'username': 'postgres',
             'password': 'postgress', 'host': 'localhost',
             'database': 'Test', 'port': '5400', 'auto_connect': True},
             {'driver_name': 'postgresql', 'username': 'postgres',
             'password': 'postgress', 'host': 'localhost',
             'database': 'usad', 'port': '5400', 'auto_connect': False}]
    

    for i in conn:
        fc.register_db_connector(i)
    
    print(f'Количество подключений: {fc.get_number_of_connections()}')
    print(f'Объекты подключения: {fc.get_db_conn_obj(conn[0])}')

    conn2 = {'driver_name': 'postgresql', 'username': 'postgres',
             'password': 'postgress', 'host': 'localhost',
             'database': 'usad', 'port': '5401', 'auto_connect': False}
    fc.register_db_connector(conn2)
    print(f'Количество подключений: {fc.get_number_of_connections()}')
    
    obj = fc.get_db_conn_obj(conn[0])
    print(obj.sql_read('select * from test_part;', 'partition'))



if __name__ == '__main__':
    main()