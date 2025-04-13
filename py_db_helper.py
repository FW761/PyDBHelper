from sqlalchemy import create_engine, URL, text
import pandas as pd


class DescriptorBase:
    def __init__(self, expected_type=str, allow_none=False):
        self.allow_none = allow_none
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value is None and self.allow_none:
            obj.__dict__[self.name] = None
        elif not isinstance(value, self.expected_type) and self.allow_none == False:
            raise TypeError(f"Значение {self.name} должно быть типа {self.expected_type.__name__}")
        else:
            obj.__dict__[self.name] = value


class Base:
    # Переменная для хранения данных подключения
    _instance = {}

    driver_name = DescriptorBase(str)
    username = DescriptorBase(str)
    password = DescriptorBase(str)
    host = DescriptorBase(str)
    database = DescriptorBase(str)
    port = DescriptorBase(str)
    connect = DescriptorBase(allow_none=True)
    engine = DescriptorBase(allow_none=True)

# --------------------------------------------------------------------------------
# Организован паттерн Singleton для того, чтобы
# была одна точка доступа к БД
    def __new__(cls,
                driver_name,
                username,
                password,
                host,
                database,
                port,
                auto_connect=False):
        key = cls._get_instance_key(driver_name,
                                    username,
                                    password,
                                    host,
                                    database,
                                    port)
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls)
        return cls._instances[key]

# ----------------------------------------------
    def __init__(self,
                 driver_name: str,
                 username: str, 
                 password: str, 
                 host: str, 
                 database: str, 
                 port: str,
                 auto_connect=False):

        self.driver_name = driver_name
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.url_object = self.create_url()
        self.engine = self.create_engine()
        self.connect = self.auto_connect() if auto_connect else None
# ----------------------------------------------

# Реализация менеджера контекста
    def __enter__(self):
        if not self._connect:
            self._connect = self.auto_connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connect()
# ----------------------------------------------

    # Создаем ссылку для подключения
    def create_url(self):
        return \
            URL.create(
                self.driver_name,
                username=self.username,
                password=self.password,  # plain (unescaped) text
                host=self.host,
                database=self.database,
                port=self.port)
    
    @classmethod
    def _get_instance_key(cls, *args):
        return hash(args)
    
    # Создаем движок для возможности подключения
    def create_engine(self):
        return create_engine(self.url_object)

    def auto_connect(self):
        return self.engine.connect()

    def close_connect(self):
        if self.connect:
            self.connect.close()

    def __repr__(self):
        status = "active" if self.connect and not self.connect.closed else "closed"
        return (f"<{self.__class__.__name__} "
                f"user='{self.username}', db='{self.database}', "
                f"host='{self.host}', port='{self.port}', status='{status}'>")
    
    def sql_read(self, query: str, schema: str = "") -> pd.DataFrame:
        """
        Выполняет SQL-запрос и возвращает результат в виде DataFrame.
        """
        if not self.connect:
            raise ConnectionError("Нет активного соединения.")

        if schema:
            self.connect.execute(text("SET search_path TO :schema"), {"schema": schema})

        return pd.read_sql(text(query), con=self.connect)

    def sql_write(self, query: str, schema: str = ""):
        """
        Выполняет SQL-запрос на изменение/запись данных.
        """
        if not self.connect:
            raise ConnectionError("Нет активного соединения.")

        if schema:
            self.connect.execute(text("SET search_path TO :schema"), {"schema": schema})

        with self.connect.begin():
            self.connect.execute(text(query))


def main():
    base = Base("postgresql",
        username="postgres",
        password="postgress",  # plain (unescaped) text
        host="localhost",
        database="usad",
        port="5400",
        auto_connect=True)

    base2 = Base("postgresql",
            username="postgres",
            password="postgress",  # plain (unescaped) text
            host="localhost",
            database="usad",
            port="5400",
            auto_connect=True)

    base3 = Base("postgresql",
            username="postgres",
            password="postgress",  # plain (unescaped) text
            host="localhost",
            database="usad",
            port="5401",
            auto_connect=False)

    print(f'Проверяем, является ли объект base и base2 одинаковыми: {base is base2}')
    print(f'Проверяем, является ли объект base и base3 одинаковыми: {base is base3}')
    print(f'Проверяем, является ли объект base2 и base3 одинаковыми: {base3 is base2}')


if __name__ == '__main__':
    main()
