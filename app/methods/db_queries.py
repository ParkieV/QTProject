import logging
import sqlite3
from datetime import datetime
from sqlite3 import Connection
from typing import Any

from app.crud.transactions_crud import TABLE_NAME, add_row
from app.settings.DBSettings import DBManager


@DBManager.db_transactions_query
def get_rows(limit: int = 30, offset: int = 0, order_create: bool = False, order_date: bool = False, order_amount: bool = False, con: Connection | None = None) -> list[Any]:
    query = f"""
        SELECT transaction_id,
            amount,
            description,
            transaction_date
        FROM {TABLE_NAME}
    """
    sort_atributes = []
    if order_create:
        sort_atributes.append("created_at")
    if order_date:
        sort_atributes.append("transaction_date")
    if order_amount:
        sort_atributes.append("amount")
    if sort_atributes:
        query += " ORDER BY " + ", ".join(sort_atributes)
        logging.info(query)
    if limit != 0:
        query += f"""
            LIMIT {limit}
            OFFSET {offset}
        """
    if con:
        result = con.execute(query).fetchall()
        return result
    else:
        raise ConnectionError("Connection to database was failed")

@DBManager.db_transactions_query
def get_amounts_group_by_date(order_date: bool = False, con: Connection | None = None) -> list[Any]:
    query = f"""
        SELECT SUM(amount),
        transaction_date
        FROM {TABLE_NAME}
        GROUP BY transaction_date
    """
    if order_date:
        query += " ORDER BY transaction_date"
    if con:
        result = con.execute(query).fetchall()
        return result
    else:
        raise ConnectionError("Connection to database was failed")

@DBManager.db_transactions_query
def get_positive_amounts_by_date(order_date: bool = False, con: Connection | None = None) -> list[Any]:
    query = f"""
        SELECT SUM(amount),
        transaction_date
        FROM {TABLE_NAME}
        WHERE amount > 0
        GROUP BY transaction_date
    """
    if order_date:
        query += " ORDER BY transaction_date"
    if con:
        result = con.execute(query).fetchall()
        return result
    else:
        raise ConnectionError("Connection to database was failed")


@DBManager.db_transactions_query
def get_negative_amounts_by_date(order_date: bool = False, con: Connection | None = None) -> list[Any]:
    query = f"""
        SELECT SUM(amount),
        transaction_date
        FROM {TABLE_NAME}
        WHERE amount < 0
        GROUP BY transaction_date
    """
    if order_date:
        query += " ORDER BY transaction_date"
    if con:
        result = con.execute(query).fetchall()
        return result
    else:
        raise ConnectionError("Connection to database was failed")


@DBManager.db_transactions_query
def get_row_count(con: Connection | None = None) -> int:
    query = f"""
        SELECT COUNT(transaction_id)
        FROM {TABLE_NAME}
    """

    if con:
        result = con.execute(query).fetchone()[0]
        return result
    else:
        raise ConnectionError("Connection to database was failed")

def upload_csv(db_path: str) -> None:
    rows = []
    with open(db_path) as f:
        rows = list(map(lambda x: x.split(';'), f.readlines()))
        if len(rows[0]) != 5:
            raise AttributeError("Количество аттрибутов не равно 5.")
        if rows[0] != ['transaction_id', 'amount', 'description', 'created_at', 'transaction_date']:
                raise ValueError("Некорректные атрибуты.")
        for i in range(1, len(rows)):
            if (not isinstance(rows[i][0], int)) and (not rows[i][0].isdigit()):
                raise ValueError(f"В строке {i} столбец {1} некорректная запись. Должно быть число")
            if (not isinstance(rows[i][1], int)) and (not rows[i][1].isdigit()):
                raise ValueError(f"В строке {i} столбец {2} некорректная запись. Должно быть число")
            try:
                datetime.strptime(rows[i][3], "%Y-%m-%d %H:%M:%S")
            except:
                raise ValueError(f"В строке {i} столбец {4} некорректная запись. Должна быть дата формата (2000-01-01 00:00:00).")
            try:
                datetime.strptime(rows[i][3], "%Y-%m-%d")
            except:
                raise ValueError(f"В строке {i} столбец {5} некорректная запись. Должна быть дата формата (2000-01-01).")
    for i in range(1, len(rows)):
        if rows[i][2]:
            data = {
                rows[0][1]: rows[i][1],
                rows[0][2]: rows[i][2],
                rows[0][3]: rows[i][3],
                rows[0][4]: rows[i][4],
            }
        else:
            data = {
                rows[0][1]: rows[i][1],
                rows[0][3]: rows[i][3],
                rows[0][4]: rows[i][4],
            }
        add_row(data)


def upload_sqlite(db_path: str) -> None:
    result = []
    with sqlite3.connect(db_path) as con_db:
        query = f"SELECT * FROM {TABLE_NAME}"
        result = con_db.execute(query).fetchall()
        print(result)
        if len(result[0]) != 5:
            raise AttributeError("Количество аттрибутов не равно 5.")
        for i in range(1, len(result)):
            if (not isinstance(result[i][0], int)) and (not result[i][0].isdigit()):
                raise ValueError(f"В строке {i + 1} столбец {1} некорректная запись. Должно быть число")
            if (not isinstance(result[i][1], int)) and (not result[i][1].isdigit()):
                raise ValueError(f"В строке {i + 1} столбец {2} некорректная запись. Должно быть число")
            try:
                datetime.strptime(result[i][3], "%Y-%m-%d %H:%M:%S")
            except:
                raise ValueError(f"В строке {i + 1} столбец {4} некорректная запись. Должна быть дата формата (2000-01-01 00:00:00).")
            try:
                datetime.strptime(result[i][4], "%Y-%m-%d")
            except:
                raise ValueError(f"В строке {i + 1} столбец {5} некорректная запись. Должна быть дата формата (2000-01-01).")
        for row in result:
            if row[2]:
                data = {
                    'amount': row[1],
                    'description': row[2],
                    'created_at': row[3],
                    'transaction_date': row[4],
                }
            else:
                data = {
                    'amount': row[1],
                    'created_at': row[3],
                    'transaction_date': row[4],
                }
            add_row(data)


if __name__=="__main__":
    print(get_negative_amounts_by_date())
