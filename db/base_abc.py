import pandas as pd
from abc import ABC, abstractmethod


class BaseABC(ABC):

    @abstractmethod
    def __init__(self, driver_name, username, password,
                 host, database, port, auto_connect=False):
        pass

    @abstractmethod
    def __new__(cls):
        return super().__new__(cls)

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create_url(self):
        pass

    @classmethod
    @abstractmethod
    def _get_instance_key(cls, *args):
        pass
    
    @abstractmethod
    def create_engine(self):
        pass

    @abstractmethod
    def auto_connect(self):
        pass

    @abstractmethod
    def close_connect(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def sql_read(self, query: str, schema: str = "") -> pd.DataFrame:
        pass

    @abstractmethod
    def sql_write(self, query: str, schema: str = ""):
        pass
