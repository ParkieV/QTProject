from PyQt5 import uic
from PyQt5.QtCore import QRegExp, QTimer
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton

from app.crud.transactions_crud import delete_row_by_id
from app.methods.db_queries import get_row_count, get_rows
from app.settings.UISettings import UI_SRC_DIR


class ExpensesWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(UI_SRC_DIR + 'expen_window.ui', self)
        self.go_back_btn_expns.clicked.connect(self.go_back_btn_fun)
        self.page = 0
        self.labels = self.findChildren(QLabel, QRegExp("spnt_lbl*"))
        self.del_buttons = self.findChildren(QPushButton, QRegExp("del_btn*"))
        self.c.clicked.connect(self._next_page)
        self.go_back.clicked.connect(self._prev_page)
        self.comboBox.currentTextChanged.connect(self._update_UI)
        self.timer = QTimer()
        self.timer.setInterval(600) # 600мс
        self.timer.timeout.connect(self._update_UI)
        self._update_UI()
        self.timer.start()

    def _update_UI(self) -> None:
        # Clear window
        for label in self.labels:
            label.hide() # type: ignore
        for del_button in self.del_buttons:
            del_button.hide() # type: ignore

        # update value
        if self.comboBox.currentIndex() == 0:
            data = get_rows(offset=self.page*30, order_date=True)
        else:
            data = get_rows(offset=self.page*30, order_amount=True)

        # idk, no time for make normal code
        if len(data) > 0:
            self.del_btn.clicked.connect(lambda: self.delete_row(data[0][0])) # type: ignore
        if len(data) > 1:
            self.del_btn_2.clicked.connect(lambda: self.delete_row(data[1][0])) # type: ignore
        if len(data) > 2:
            self.del_btn_3.clicked.connect(lambda: self.delete_row(data[2][0])) # type: ignore
        if len(data) > 3:
            self.del_btn_4.clicked.connect(lambda: self.delete_row(data[3][0])) # type: ignore
        if len(data) > 4:
            self.del_btn_5.clicked.connect(lambda: self.delete_row(data[4][0])) # type: ignore
        if len(data) > 5:
            self.del_btn_6.clicked.connect(lambda: self.delete_row(data[5][0])) # type: ignore
        if len(data) > 6:
            self.del_btn_7.clicked.connect(lambda: self.delete_row(data[6][0])) # type: ignore
        if len(data) > 7:
            self.del_btn_8.clicked.connect(lambda: self.delete_row(data[7][0])) # type: ignore
        if len(data) > 8:
            self.del_btn_9.clicked.connect(lambda: self.delete_row(data[8][0])) # type: ignore
        if len(data) > 9:
            self.del_btn_10.clicked.connect(lambda: self.delete_row(data[9][0])) # type: ignore
        if len(data) > 10:
            self.del_btn_11.clicked.connect(lambda: self.delete_row(data[10][0])) # type: ignore
        if len(data) > 11:
            self.del_btn_12.clicked.connect(lambda: self.delete_row(data[11][0])) # type: ignore
        if len(data) > 12:
            self.del_btn_13.clicked.connect(lambda: self.delete_row(data[12][0])) # type: ignore
        if len(data) > 13:
            self.del_btn_14.clicked.connect(lambda: self.delete_row(data[13][0])) # type: ignore
        if len(data) > 14:
            self.del_btn_15.clicked.connect(lambda: self.delete_row(data[14][0])) # type: ignore
        if len(data) > 15:
            self.del_btn_16.clicked.connect(lambda: self.delete_row(data[15][0])) # type: ignore
        if len(data) > 16:
            self.del_btn_17.clicked.connect(lambda: self.delete_row(data[16][0])) # type: ignore
        if len(data) > 17:
            self.del_btn_18.clicked.connect(lambda: self.delete_row(data[17][0])) # type: ignore
        if len(data) > 18:
            self.del_btn_19.clicked.connect(lambda: self.delete_row(data[18][0])) # type: ignore
        if len(data) > 19:
            self.del_btn_20.clicked.connect(lambda: self.delete_row(data[19][0])) # type: ignore
        if len(data) > 20:
            self.del_btn_21.clicked.connect(lambda: self.delete_row(data[20][0])) # type: ignore
        if len(data) > 21:
            self.del_btn_22.clicked.connect(lambda: self.delete_row(data[21][0])) # type: ignore
        if len(data) > 22:
            self.del_btn_23.clicked.connect(lambda: self.delete_row(data[22][0])) # type: ignore
        if len(data) > 23:
            self.del_btn_24.clicked.connect(lambda: self.delete_row(data[23][0])) # type: ignore
        if len(data) > 24:
            self.del_btn_25.clicked.connect(lambda: self.delete_row(data[24][0])) # type: ignore
        if len(data) > 25:
            self.del_btn_26.clicked.connect(lambda: self.delete_row(data[25][0])) # type: ignore
        if len(data) > 26:
            self.del_btn_27.clicked.connect(lambda: self.delete_row(data[26][0])) # type: ignore
        if len(data) > 27:
            self.del_btn_28.clicked.connect(lambda: self.delete_row(data[27][0])) # type: ignore
        if len(data) > 28:
            self.del_btn_29.clicked.connect(lambda: self.delete_row(data[28][0])) # type: ignore
        if len(data) > 29:
            self.del_btn_30.clicked.connect(lambda: self.delete_row(data[29][0])) # type: ignore
        for i in range(len(data)):
            self.labels[i].setText(str(data[i][1]) + "\t" + str(data[i][2]) + "\t" + str(data[i][3])) # type: ignore
            self.labels[i].show() # type: ignore
            self.del_buttons[i].show() # type: ignore

    def delete_row(self, id: int) -> None:
        print(id)
        delete_row_by_id(id)

    def _next_page(self):
        row_count = get_row_count()
        if self.page < row_count // 30:
            self.page += 1

        self._update_UI()


    def _prev_page(self):
        if self.page > 0:
            self.page -= 1

        self._update_UI()

    def go_back_btn_fun(self) -> None:
        self.page = 0
        self.hide()
