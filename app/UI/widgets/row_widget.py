from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QWidget

from app.UI.widgets.button_widgets import DeleteButton


class RowWidget(QWidget):
    def __init__(self, size: QSize, text: str = '') -> None:
        super().__init__()
        self.setFixedSize(size)
        self.text_widget = QLabel()
        self.text_widget.setText(text)
        self.delete_widget = DeleteButton()
