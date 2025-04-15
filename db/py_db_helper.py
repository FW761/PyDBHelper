import pandas as pd
from .base_abc import BaseABC
from .descriptor_base import DescriptorBase
from sqlalchemy import create_engine, URL, text


class Base(BaseABC):
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
    def __new__(cls, driver_name, username, password, host,
                database, port, auto_connect=False):
        key = cls._get_instance_key(driver_name, username, password,
                                    host, database, port)
        if key not in cls._instance:
            cls._instance[key] = super().__new__(cls)
        return cls._instance[key]

# ----------------------------------------------
    def __init__(self, driver_name: str, username: str,  password: str, 
                 host: str, database: str, port: str, auto_connect=False):
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
        try:
            self.close_connect()
        except Exception as e:
            print(f"Ошибка при закрытии соединения: {e}")
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

    # Python не гарантирует одинаковый результат между разными запусками
    # программы, если не зафиксирован PYTHONHASHSEED
    # по этой причине, код был исправлен и вместо hash,
    # преобразуем элементы в строку
    @classmethod
    def _get_instance_key(cls, *args):
        return str(args)

    # Создаем движок для возможности подключения
    def create_engine(self):
        return create_engine(self.url_object)

    def auto_connect(self):
        return self.engine.connect()

    def close_connect(self):
        if self.connect:
            self.connect.close()

    def __repr__(self):
        status = "active" if self.connect and not \
                        self.connect.closed else "closed"
        return f"<{self.__class__.__name__} \
                    [{status}] {self.username}@{self.host}: \
                        {self.port}/{self.database}>"
   
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

