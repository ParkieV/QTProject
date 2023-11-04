import logging
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from app.crud.transactions_crud import delete_row_by_id
from app.methods.db_queries import get_rows, upload_csv, upload_sqlite
from app.methods.matrix_tools import transpose
from app.settings.DBSettings import DATABASE_DIR
from app.settings.UISettings import UI_SRC_DIR
from app.UI.windows.ExpensesWindow import ExpensesWindow
from app.UI.windows.GraphicsWindow import GraphicsWindow


class DatabaseWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.graph_values = None
        self.input_database = None
        logging.info(f"Path to UI srcs: {UI_SRC_DIR}")
        uic.loadUi(UI_SRC_DIR + 'untitled.ui', self)
        self.expenses_window = ExpensesWindow()
        self.graphics_window = GraphicsWindow()
        self.month_days_from_start_of_year = {
            1: 31,  # Январь
            2: 31 + 28,  # Февраль
            3: 31 + 28 + 31,  # Март
            4: 31 + 28 + 31 + 30,  # Апрель
            5: 31 + 28 + 31 + 30 + 31,  # Май
            6: 31 + 28 + 31 + 30 + 31 + 30,  # Июнь
            7: 31 + 28 + 31 + 30 + 31 + 30 + 31,  # Июль
            8: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31,  # Август
            9: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30,  # Сентябрь
            10: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31,  # Октябрь
            11: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30,  # Ноябрь
            12: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31  # Декабрь
        }

        self.build_plot()
        self._init_ui()

    def _init_ui(self) -> None:
        self.redact_btn_1.hide()
        self.redact_btn_2.hide()
        self.redact_btn_3.hide()
        self.redact_btn_4.hide()
        self.redact_btn_5.hide()
        self.redact_btn_6.hide()
        self.redact_btn_7.hide()

        self.del_btn_1.hide()
        self.del_btn_2.hide()
        self.del_btn_3.hide()
        self.del_btn_4.hide()
        self.del_btn_5.hide()
        self.del_btn_6.hide()
        self.del_btn_7.hide()

        self.spnt_lbl_1.hide()
        self.spnt_lbl_2.hide()
        self.spnt_lbl_3.hide()
        self.spnt_lbl_4.hide()
        self.spnt_lbl_5.hide()
        self.spnt_lbl_6.hide()
        self.spnt_lbl_7.hide()

        self.last_spends_fun()

        self.all_spents_btn.clicked.connect(self.all_spents_btn_fun)
        self.all_graph_btn.clicked.connect(self.all_graph_btn_fun)
        self.download_btn_.clicked.connect(self.download_btn__fun)
        self.download_btn.clicked.connect(self.download_btn_fun)

    def download_btn_fun(self) -> None:
        self.input_database = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        print(self.input_database)
        if self.input_database[self.input_database.rfind('.') +1:] == "sqlite":
            upload_sqlite(self.input_database)
        elif self.input_database[self.input_database.rfind('.') +1:] == "csv":
            upload_csv(self.input_database)
        elif self.input_database != '':
            raise ValueError("Uncorrect format of file. Should be '.csv' or '.sqlite'.")
        self.last_spends_fun()

    def build_plot(self) -> None:
        if data := transpose(get_rows(0)):
            y_graph_list = data[1]
            x_date_day = map(lambda x: x[x.rfind('-') + 1:], data[-1])
            x_date_mon = map(lambda x: x[x.find('-') + 1: x.rfind('-')], data[-1])
            x_date_year = map(lambda x: x[: x.find('-')], data[-1])
            print(x_date_day, x_date_mon, x_date_year, sep="\n\n")
            # self.graph_values - матрица, в которой хранятся два списка:
            # 1-ый содержит количество дней прошедших с начала добавления первого дохода \ расхода
            # 2-ой содержит все расходы введённые пользователь на момент инициализации программы

            print(list(x_date_day))
            self.graph_values = [[list(x_date_day)[i] +
                                  self.month_days_from_start_of_year[list(x_date_mon)[i]] +
                                  (365 * list(x_date_year)[i]) -
                                  list(x_date_day)[0] +
                                  self.month_days_from_start_of_year[list(x_date_mon)[0]] +
                                  (365 * list(x_date_year)[0])
                                  for i in range(len(list(x_date_day)))],
                                 list(y_graph_list)
                                 ]

            self.graph_main_pg.clear()
            self.graph_main_pg.plot(self.graph_values[0], self.graph_values[1])

    def last_spends_fun(self) -> None:
        self.last_spends_transactions = get_rows(7, order_date=True)

        if len(self.last_spends_transactions) >= 1:
            self.spnt_lbl_1.setText(str(self.last_spends_transactions[0][1]) + "\t" + str(self.last_spends_transactions[0][2]) + "\t" + str(self.last_spends_transactions[0][3]))
            self.spnt_lbl_1.show()
            self.del_btn_1.show()
            self.del_btn_1.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[0][0]))

        if len(self.last_spends_transactions) >= 2:
            self.spnt_lbl_2.setText(str(self.last_spends_transactions[1][1]) + "\t" + str(self.last_spends_transactions[1][2]) + "\t" + str(self.last_spends_transactions[1][3]))
            self.spnt_lbl_2.show()
            self.del_btn_2.show()
            self.del_btn_2.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[1][0]))

        if len(self.last_spends_transactions) >= 3:
            self.spnt_lbl_3.setText(str(self.last_spends_transactions[2][1]) + "\t" + str(self.last_spends_transactions[2][2]) + "\t" + str(self.last_spends_transactions[2][3]))
            self.spnt_lbl_3.show()
            self.del_btn_3.show()
            self.del_btn_3.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[2][0]))

        if len(self.last_spends_transactions) >= 4:
            self.spnt_lbl_4.setText(str(self.last_spends_transactions[3][1]) + "\t" + str(self.last_spends_transactions[3][2]) + "\t" + str(self.last_spends_transactions[3][3]))
            self.spnt_lbl_4.show()
            self.del_btn_4.show()
            self.del_btn_4.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[3][0]))

        if len(self.last_spends_transactions) >= 5:
            self.spnt_lbl_5.setText(str(self.last_spends_transactions[4][1]) + "\t" + str(self.last_spends_transactions[4][2]) + "\t" + str(self.last_spends_transactions[4][3]))
            self.spnt_lbl_5.show()
            self.del_btn_5.show()
            self.del_btn_5.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[4][0]))

        if len(self.last_spends_transactions) >= 6:
            self.spnt_lbl_6.setText(str(self.last_spends_transactions[5][1]) + "\t" + str(self.last_spends_transactions[5][2]) + "\t" + str(self.last_spends_transactions[5][3]))
            self.spnt_lbl_6.show()
            self.del_btn_6.show()
            self.del_btn_6.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[5][0]))

        if len(self.last_spends_transactions) >= 7:
            self.spnt_lbl_7.setText(str(self.last_spends_transactions[6][1]) + "\t" + str(self.last_spends_transactions[6][2]) + "\t" + str(self.last_spends_transactions[6][3]))
            self.spnt_lbl_7.show()
            self.del_btn_7.show()
            self.del_btn_7.clicked.connect(lambda: self.delete_row_button(self.last_spends_transactions[6][0]))

    def delete_row_button(self, id: int) -> None:
        delete_row_by_id(id)
        self.last_spends_fun()

    def download_btn__fun(self, **kwargs) -> None:
        try:
            date_day = int(self.date_line.text().split(".")[0])
            date_mon = int(self.date_line.text().split(".")[1])
            date_year = int(self.date_line.text().split(".")[2])

            con = sqlite3.connect(DATABASE_DIR + 'Expenses_database.sqlite')

            with con:
                query = f"""
                    INSERT INTO financial_transactions_test
                    (sum_of_pay, describe, date_day, date_mon, date_year)
                     VALUES
                    ({int(self.sum_line.text())}, {self.dscribe_line.text()}, {date_day}, {date_mon}, {date_year})
                """

                con.execute(query)

            con.close()

        except Exception as err:
            logging.error(str(err))

        self.last_spends_fun()

    def all_spents_btn_fun(self) -> None:
        self.expenses_window.show()

    def all_graph_btn_fun(self) -> None:
        self.graphics_window.show()
