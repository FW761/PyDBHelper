import re
from db import py_db_helper


class FactoryConnect:
    _DB_CONNECTIONS = {} #Список подключения к БД
    supported_drivers = {"postgresql"}  # Сет поддерживаемых драйверов

    def __init__(self):
        pass

    @classmethod
    def register_db_connector(cls, conn: dict):
        key = cls._get_instance_key(conn)
        if key not in cls._DB_CONNECTIONS:
            cls._DB_CONNECTIONS[key] = py_db_helper.Base(**conn)
    
    @classmethod
    def get_db_conn_obj(cls, conn: dict):
        key = cls._get_instance_key(conn)
        if key not in cls._DB_CONNECTIONS:
            return None
        return cls._DB_CONNECTIONS[key]

    @classmethod
    def _get_instance_key(cls, args: dict):
        return str(list(args.values())[0:-1:1])

    @classmethod
    def add_supported_driver(cls, driver_name: str):
        """Добавить новый поддерживаемый драйвер"""
        cls.supported_drivers.add(driver_name.lower())

    @classmethod
    def delate_supported_driver(cls, driver_name: str):
        """Добавить новый поддерживаемый драйвер"""
        cls.supported_drivers.remove(driver_name.lower())

    @classmethod
    def get_number_of_connections(cls):
        return len(cls._DB_CONNECTIONS)

    @classmethod
    def _check_param(cls, driver_name, username, password,
                     host, database, port, *args):

        if not isinstance(driver_name, str) or driver_name.lower() not in cls.supported_drivers:
            raise ValueError(f"Поддерживаемые драйверы: {cls.supported_drivers}. Получено: {driver_name}")

        if not isinstance(username, str) or not username:
            raise ValueError("Имя пользователя должно быть строкой и не пустым.")

        if not isinstance(password, str):
            raise ValueError("Пароль должен быть строкой.")

        if not isinstance(host, str) or not re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^[\w.-]+$', host):
            raise ValueError(f"Некорректный адрес хоста: {host}")

        if not isinstance(database, str) or not database:
            raise ValueError("Название базы данных должно быть строкой и не пустым.")

        if not isinstance(port, (int)) or not (1 <= int(port) <= 65535):
            raise ValueError(f"Некорректный порт: {port}")
