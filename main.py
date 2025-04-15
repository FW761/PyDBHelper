from db import py_db_helper

def main():
    base = py_db_helper.Base("postgresql", username="postgres", password="postgress",
                host="localhost", database="usad", port="5400", auto_connect=False)

    base2 = py_db_helper.Base("postgresql", username="postgres", password="postgress",
                 host="localhost", database="usad", port="5400", auto_connect=False)

    base3 = py_db_helper.Base("postgresql", username="postgres", password="postgress",
                 host="localhost", database="usad", port="5401", auto_connect=False)

    print(f'Проверяем, является ли объект base и base2 одинаковыми: {base is base2}')
    print(f'Проверяем, является ли объект base и base3 одинаковыми: {base is base3}')
    print(f'Проверяем, является ли объект base2 и base3 одинаковыми: {base3 is base2}')


if __name__ == '__main__':
    main()