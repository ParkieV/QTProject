from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.methods.db_queries import get_row_count, get_rows
from app.settings.UISettings import UI_SRC_DIR


class ExpensesWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(UI_SRC_DIR + 'expen_window.ui', self)
        self.go_back_btn_expns.clicked.connect(self.go_back_btn_fun)
        self.page = 0

    def _update_UI(self) -> None:
        custom_table = [self.verticalLayout, self.verticalLayout_2, self.verticalLayout_3]

        #clear window
        for column in custom_table:
            for i_row in range(column.count()):
                 for i_elem in range(column.itemAt(i_row).count()):
                      column.itemAt(i_row).itemAt(i_elem).widget().hide()

        # update value
        if self.comboBox.currentIndex == 0:
            data = get_rows(offset=self.page*30, order_date=True)
        else:
            data = get_rows(offset=self.page*30, order_amount=True)
        for i in range(len(data)):
            custom_table[i//10].itemAt(i%10).itemAt(0).widget().setText(str(data[i][1]) + "\t" + str(data[i][2]) + "\t" + str(data[i][3]))
            for i_elem in range(custom_table[i//10].itemAt(i%10).count()):
                custom_table[i//10].itemAt(i%10).itemAt(i_elem).widget().show()

    def _next_page(self):
        row_count = get_row_count()
        if row_count % 30 == 0:
            if self.page < row_count // 30:
                self.page += 1
        else:
            if self.page < row_count // 30 + 1:
                self.page += 1

        self._update_UI()


    def _prev_page(self):
        if self.page > 0:
            self.page -= 1

        self._update_UI()

    def go_back_btn_fun(self) -> None:
        self.page = 0
        self.hide()
