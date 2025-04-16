import re
from db import py_db_helper


class FactoryConnect:
    _DB_CONNECTIONS = {} #Список подключения к БД
    supported_drivers = {"postgresql"}  # Сет поддерживаемых драйверов

    def __init__(self):
        pass

    @classmethod
    def register_db_connector(cls, conn: list):
        key = cls._get_instance_key(*conn)
        if key is not cls._DB_CONNECTIONS:
            cls._DB_CONNECTIONS[conn] = py_db_helper.Base()

    @classmethod
    def _get_instance_key(cls, *args):
        return str(args)

    @classmethod
    def add_supported_driver(cls, driver_name: str):
        """Добавить новый поддерживаемый драйвер"""
        cls.supported_drivers.add(driver_name.lower())

    @classmethod
    def _check_param(cls, driver_name, username, password, host, database, port, *args):

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

        if not isinstance(port, (str, int)) or not str(port).isdigit() or not (1 <= int(port) <= 65535):
            raise ValueError(f"Некорректный порт: {port}")
