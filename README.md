# Класс Base для работы с базой данных через SQLAlchemy

Класс `Base` реализует подключение к базе данных с помощью SQLAlchemy и использует паттерн Singleton, чтобы избежать создания нескольких подключений с одинаковыми параметрами.

## 📦 Основные возможности

- Поддержка только одного подключения на уникальный набор параметров (`host`, `port`, `user` и т.д.).
- Использует контекстный менеджер (`with Base(...) as db`) для автоматического открытия/закрытия соединения.
- Поддержка чтения SQL-запросов через Pandas (`sql_read()`).
- Контроль типов и допуска `None` через дескрипторы (`DescriptorBase`).
- Гибкое подключение: сразу (`auto_connect=True`) или вручную.

## 🔧 Атрибуты

| Атрибут       | Тип     | Описание                        |
|---------------|---------|----------------------------------|
| `driver_name` | `str`   | Название драйвера (например, `'postgresql'`) |
| `username`    | `str`   | Имя пользователя                 |
| `password`    | `str`   | Пароль пользователя              |
| `host`        | `str`   | Хост БД                         |
| `database`    | `str`   | Имя базы данных                  |
| `port`        | `str`   | Порт                             |
| `connect`     | объект подключения SQLAlchemy, или `None` |
| `engine`      | SQLAlchemy Engine                        |

## 🔨 Методы

### `__new__(...)`
Переопределённый метод `__new__`, который реализует паттерн Singleton.

### `create_url() -> sqlalchemy.engine.URL`
Создаёт URL для подключения.

### `create_engine() -> sqlalchemy.Engine`
Создаёт движок SQLAlchemy на основе URL.

### `auto_connect() -> sqlalchemy.Connection`
Осуществляет подключение.

### `close_connect()`
Закрывает соединение.

### `sql_read(query: str, schema: str = '') -> pd.DataFrame`
Выполняет SQL-запрос и возвращает `DataFrame`.

## 🔁 Пример использования

```python
with Base(
    driver_name="postgresql",
    username="user",
    password="pass",
    host="localhost",
    database="db",
    port="5432",
    auto_connect=True
) as db:
    df = db.sql_read("SELECT * FROM my_table")
