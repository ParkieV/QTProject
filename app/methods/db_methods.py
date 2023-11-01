from sqlite3 import Connection
from typing import Any

from app.crud.transactions_crud import TABLE_NAME
from app.settings.DBSettings import DBManager


@DBManager.db_transactions_query
def get_rows(limit: int = 30, offset: int = 0, con: Connection | None = None) -> list[Any]:
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        LIMIT {limit}
        OFFSET {offset};
    """
    if con:
        result = con.execute(query).fetchall()
        return result
    else:
        raise ConnectionError("Connection to database was failed")


if __name__=="__main__":
    print(get_rows())
