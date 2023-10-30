import logging
import sys

from PyQt5.QtWidgets import QApplication

from app.UI.DatabaseWindow import DatabaseWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        filename="app/db_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s\t%(message)s")
    app = QApplication(sys.argv)
    ex = DatabaseWindow()
    ex.show()
    sys.exit(app.exec_())
