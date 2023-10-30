from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.settings.UISettings import UI_SRC_DIR


class GraphicsWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(UI_SRC_DIR + 'graph_window.ui', self)
        self.go_back_btn_graph.clicked.connect(self.go_back_btn_fun)


    def go_back_btn_fun(self) -> None:
        self.hide()
