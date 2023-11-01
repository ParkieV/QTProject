import logging
import os
import sys
from sqlite3 import Connection

sys.path.append(os.getcwd())

from app.methods.validate_query import validate_query_values
from app.settings.DBSettings import DBManager

TABLE_NAME = "financial_transactions"

@DBManager.db_transactions_query
@validate_query_values
def add_row(values: dict, con: Connection | None = None) -> int:
    query = f"""
            INSERT into {TABLE_NAME}
                ({", ".join(values)})
            VALUES
                ({", ".join(map(str, values.values()))})
            RETURNING transaction_id;
        """
    logging.info(f"SQL query is {query}")
    if con:
        result = con.execute(query).fetchone()[0]
        return result
    else:
        raise ConnectionError("Connection to database was failed")

@DBManager.db_transactions_query
def get_row_by_id(id: int, con: Connection | None = None) -> dict:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE transaction_id = {id};
    """
    logging.info(f"SQL query is {query}")
    if con:
        result = con.execute(query).fetchone()
        return result
    else:
        raise ConnectionError("Connection to database was failed")

@DBManager.db_transactions_query
@validate_query_values
def update_row_by_id(values: dict, id: int, con: Connection | None = None) -> int:
    query = f"""
            UPDATE {TABLE_NAME}
                SET {", ".join(map(lambda k: f"{k} = {values[k]}", values))}
            WHERE transaction_id = {id}
            RETURNING transaction_id;
        """
    logging.info(f"SQL query is {query}")
    if con:
        result = con.execute(query).fetchone()[0]
        return result
    else:
        raise ConnectionError("Connection to database was failed")

@DBManager.db_transactions_query
def delete_row_by_id(id: int, con: Connection | None = None) -> None:
    query = f"""
        DELETE from {TABLE_NAME}
        WHERE transaction_id = {id};
    """
    if con:
        con.execute(query)
    else:
        raise ConnectionError("Connection to database was failed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filename="app/db_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s\t%(message)s")
    add_row(values={"amount": 100,
        "transaction_date": "2021-11-30"})
    print(get_row_by_id(10))
    update_row_by_id(values={"amount": 101}, id=10)
    print(get_row_by_id(10))
    delete_row_by_id(10)

