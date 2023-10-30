import os
import sqlite3
from sqlite3 import Connection
from typing import Any, Generator

DATABASE_DIR = os.getcwd() + "/database/"

class DBManager:
    @staticmethod
    def get_connection() -> Generator[Connection, Any, None]:
        with sqlite3.connect('Expenses_database.sqlite') as con:
            yield con

    @staticmethod
    def check_connection(con: Connection) -> None:
        pass

    @staticmethod
    def close_connection(con: Connection) -> None:
        con.commit()
        con.close()

