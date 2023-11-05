import logging
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from app.crud.transactions_crud import add_row, delete_row_by_id
from app.methods.db_queries import get_rows, upload_csv, upload_sqlite
from app.methods.matrix_tools import transpose
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
        self.del_id = 0
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
        if self.input_database[self.input_database.rfind('.') +1:] == "sqlite":
            upload_sqlite(self.input_database)
        elif self.input_database[self.input_database.rfind('.') +1:] == "csv":
            upload_csv(self.input_database)
        elif self.input_database != '':
            raise ValueError("Uncorrect format of file. Should be '.csv' or '.sqlite'.")
        self.last_spends_fun()

    def build_plot(self) -> None:
        if data := transpose(get_rows(0, order_date=True)):
            y_amount_graph_list = data[1]
            x_date_day = data[-1]
            # self.graph_values - матрица, в которой хранятся два списка:
            # 1-ый содержит количество дней прошедших с начала добавления первого дохода \ расхода
            # 2-ой содержит все расходы введённые пользователь на момент инициализации программы

            self.graph_values = [list(map(lambda x: (datetime.strptime(x, "%Y-%m-%d")-datetime.strptime(x_date_day[0], "%Y-%m-%d")).days, x_date_day)),
                                 y_amount_graph_list
                                 ]

            self.graph_main_pg.clear()
            self.graph_main_pg.plot(self.graph_values[0], self.graph_values[1])

    def last_spends_fun(self) -> None:
        self.last_spends_transactions = get_rows(7, order_date=True, desc=True)

        if len(self.last_spends_transactions) >= 1:
            self.spnt_lbl_1.setText(str(self.last_spends_transactions[0][1]) + "\t" + str(self.last_spends_transactions[0][2]) + "\t" + str(self.last_spends_transactions[0][3]))
            self.spnt_lbl_1.show()
            self.del_btn_1.show()
            self.del_btn_1.clicked.connect(self.delete_row_button(self.last_spends_transactions[0][0]))

        if len(self.last_spends_transactions) >= 2:
            self.spnt_lbl_2.setText(str(self.last_spends_transactions[1][1]) + "\t" + str(self.last_spends_transactions[1][2]) + "\t" + str(self.last_spends_transactions[1][3]))
            self.spnt_lbl_2.show()
            self.del_btn_2.show()
            self.del_btn_2.clicked.connect(self.delete_row_button(self.last_spends_transactions[1][0]))

        if len(self.last_spends_transactions) >= 3:
            self.spnt_lbl_3.setText(str(self.last_spends_transactions[2][1]) + "\t" + str(self.last_spends_transactions[2][2]) + "\t" + str(self.last_spends_transactions[2][3]))
            self.spnt_lbl_3.show()
            self.del_btn_3.show()
            self.del_btn_3.clicked.connect(self.delete_row_button(self.last_spends_transactions[2][0]))

        if len(self.last_spends_transactions) >= 4:
            self.spnt_lbl_4.setText(str(self.last_spends_transactions[3][1]) + "\t" + str(self.last_spends_transactions[3][2]) + "\t" + str(self.last_spends_transactions[3][3]))
            self.spnt_lbl_4.show()
            self.del_btn_4.show()
            self.del_btn_4.clicked.connect(self.delete_row_button(self.last_spends_transactions[3][0]))

        if len(self.last_spends_transactions) >= 5:
            self.spnt_lbl_5.setText(str(self.last_spends_transactions[4][1]) + "\t" + str(self.last_spends_transactions[4][2]) + "\t" + str(self.last_spends_transactions[4][3]))
            self.spnt_lbl_5.show()
            self.del_btn_5.show()
            self.del_btn_5.clicked.connect(self.delete_row_button(self.last_spends_transactions[4][0]))

        if len(self.last_spends_transactions) >= 6:
            self.spnt_lbl_6.setText(str(self.last_spends_transactions[5][1]) + "\t" + str(self.last_spends_transactions[5][2]) + "\t" + str(self.last_spends_transactions[5][3]))
            self.spnt_lbl_6.show()
            self.del_btn_6.show()
            self.del_btn_6.clicked.connect(self.delete_row_button(self.last_spends_transactions[5][0]))

        if len(self.last_spends_transactions) >= 7:
            self.spnt_lbl_7.setText(str(self.last_spends_transactions[6][1]) + "\t" + str(self.last_spends_transactions[6][2]) + "\t" + str(self.last_spends_transactions[6][3]))
            self.spnt_lbl_7.show()
            self.del_btn_7.show()
            self.del_btn_7.clicked.connect(self.delete_row_button(self.last_spends_transactions[6][0]))

    def delete_row_button(self, id: int) -> None:
        print(id)
        delete_row_by_id(id)
        self.last_spends_fun()

    def download_btn__fun(self, **kwargs) -> None:
        data = {
            "amount": int(self.sum_line.text()),
            "description": self.dscribe_line.text(),
            "transaction_date": '-'.join(reversed(self.date_line.text().split('.')))
        }
        add_row(data)

        self.last_spends_fun()

    def all_spents_btn_fun(self) -> None:
        self.expenses_window.show()

    def all_graph_btn_fun(self) -> None:
        self.graphics_window.show()
