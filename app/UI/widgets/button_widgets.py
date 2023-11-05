from PyQt5.QtWidgets import QPushButton


class DeleteButton(QPushButton):
    def __init__(self) -> None:
        super().__init__()
        self.setText('🗑')
        self.setStyleSheet("""QPushButton{
	background-color: rgb(242, 71, 38);
	color: rgb(255, 255, 255);
	border-radius: 5px;
	font-size: 16px;
}
QPushButton:pressed {
	background-color: rgb(39, 45, 30);
}""")
