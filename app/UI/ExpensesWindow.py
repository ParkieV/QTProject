from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.settings.UISettings import UI_SRC_DIR


class ExpensesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_SRC_DIR + 'expen_window.ui', self)
        self.go_back_btn_expns.clicked.connect(self.go_back_btn_fun)

    def go_back_btn_fun(self) -> None:
        self.hide()
