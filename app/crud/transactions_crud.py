import os
import sys
from sqlite3 import Connection

sys.path.append(os.getcwd())
print(sys.path)

from app.methods.validate_query import validate_query_values
from app.settings.DBSettings import DBManager


class TransactionsCRUD:
    DB_NAME = "financial_transactions_test"

    def __init__(self) -> None:
        if DBManager.check_connection():
            pass
        else:
            pass
            # raise ConnectionError("Connect to database was failed.")

    @validate_query_values
    @DBManager.db_transactions_query
    @staticmethod
    def add_row(values: dict, con: Connection | None = None) -> int:
        insert_attribute = list(values.keys())
        query = f"""
                INSERT into {TransactionsCRUD.DB_NAME}
                    ({", ".join(insert_attribute)})
                VALUES
                    ({", ".join(map(str, values.values()))})
                RETURNING transaction_id;
            """
        if con:
            result = con.execute(query).fetchone()[0]
            return result
        else:
            raise ConnectionError("Connection to database was failed")
if __name__=="__main__":
    TransactionsCRUD()
    TransactionsCRUD.add_row(values={"amount": 100,
                              "transaction_date": "2021-11-30"})
