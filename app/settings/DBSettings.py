import os
import sqlite3

DATABASE_DIR = os.getcwd() + "/database/"
DATABASE_NAME = ''

class DBManager:

    @staticmethod
    def db_transactions_query(func):
        def called(*args, **kwargs):
            with sqlite3.connect(DATABASE_DIR + 'Expenses_database.sqlite') as con:
                result = func(con=con, *args, **kwargs)
                return result
        return called

    @staticmethod
    def check_connection(db_path: str) -> bool:
        try:
            con = sqlite3.connect(db_path)
            query = """
                SELECT 1
                FROM financial_transactions;
            """

            con.execute(query)
            con.commit()
            con.close()

            return True

        except Exception:
            return False

