from sqlite3 import Connection
from typing import Any

from app.crud.transactions_crud import TABLE_NAME
from app.settings.DBSettings import DBManager


@DBManager.db_transactions_query
def get_rows(limit: int = 30, offset: int = 0, order_create: bool = False, order_date: bool = False, order_amount: bool = False, con: Connection | None = None) -> list[Any]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        LIMIT {limit}
        OFFSET {offset}
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


if __name__=="__main__":
    print(get_negative_amounts_by_date())
