import logging
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.settings.DBSettings import DATABASE_DIR
from app.settings.UISettings import UI_SRC_DIR
from app.UI.windows.ExpensesWindow import ExpensesWindow
from app.UI.windows.GraphicsWindow import GraphicsWindow


class DatabaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info(f"Path to UI srcs: {UI_SRC_DIR}")
        uic.loadUi(UI_SRC_DIR + 'untitled.ui', self)
        self.expenses_window = ExpensesWindow()
        self.graphics_window = GraphicsWindow()

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

    def last_spends_fun(self) -> None:
        con = sqlite3.connect(DATABASE_DIR + 'Expenses_database.sqlite')
        cur = con.cursor()

        result = cur.execute("""SELECT * FROM expnstable""")
        result = sorted(result, key=lambda x: x[2])
        result = sorted(result, key=lambda x: x[3])
        result = sorted(result, key=lambda x: x[4])
        print(result)

        if len(result) >= 1:
            self.spnt_lbl_1.setText(str(result[0][0]) + "\t" + str(result[0][1]) + "\t" + str(result[0][2]) + "." +
                                    str(result[0][3]))
            self.spnt_lbl_1.show()
            self.redact_btn_1.show()
            self.redact_btn_1.show()
            self.del_btn_1.show()

        if len(result) >= 2:
            self.spnt_lbl_2.setText(str(result[1][0]) + "\t" + str(result[1][1]) + "\t" + str(result[1][2]) + "." +
                                    str(result[1][3]) + "." + str(result[1][4]))
            self.spnt_lbl_2.show()
            self.redact_btn_2.show()
            self.redact_btn_2.show()
            self.del_btn_2.show()

        if len(result) >= 3:
            self.spnt_lbl_3.setText(str(result[2][0]) + "\t" + str(result[2][1]) + "\t" + str(result[2][2]) + "." +
                                    str(result[2][3]) + "." + str(result[2][4]))
            self.spnt_lbl_3.show()
            self.redact_btn_3.show()
            self.redact_btn_3.show()
            self.del_btn_3.show()

        if len(result) >= 4:
            self.spnt_lbl_4.setText(str(result[3][0]) + "\t" + str(result[3][1]) + "\t" + str(result[3][2]) + "." +
                                    str(result[3][3]) + "." + str(result[3][4]))
            self.spnt_lbl_4.show()
            self.redact_btn_4.show()
            self.redact_btn_4.show()
            self.del_btn_4.show()

        if len(result) >= 5:
            self.spnt_lbl_5.setText(str(result[4][0]) + "\t" + str(result[4][1]) + "\t" + str(result[4][2]) + "." +
                                    str(result[4][3]) + "." + str(result[4][4]))
            self.spnt_lbl_5.show()
            self.redact_btn_5.show()
            self.redact_btn_5.show()
            self.del_btn_5.show()

        if len(result) >= 6:
            self.spnt_lbl_6.setText(str(result[5][0]) + "\t" + str(result[5][1]) + "\t" + str(result[5][2]) + "." +
                                    str(result[5][3]) + "." + str(result[5][4]))
            self.spnt_lbl_6.show()
            self.redact_btn_6.show()
            self.redact_btn_6.show()
            self.del_btn_6.show()

        if len(result) >= 7:
            self.spnt_lbl_7.setText(str(result[6][0]) + "\t" + str(result[6][1]) + "\t" + str(result[6][2]) + "." +
                                    str(result[6][3]) + "." + str(result[6][4]))
            self.spnt_lbl_7.show()
            self.redact_btn_7.show()
            self.redact_btn_7.show()
            self.del_btn_7.show()

    def download_btn__fun(self, **kwargs):
        try:
            date_day = int(self.date_line.text().split(".")[0])
            date_mon = int(self.date_line.text().split(".")[1])
            date_year = int(self.date_line.text().split(".")[2])

            con = sqlite3.connect(DATABASE_DIR + 'Expenses_database.sqlite')

            with con:
                query = f"""
                    INSERT INTO expnstable
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
