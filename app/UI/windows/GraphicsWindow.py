import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.settings.DBSettings import DATABASE_DIR
from app.settings.UISettings import UI_SRC_DIR


class GraphicsWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.graph_values = None
        uic.loadUi(UI_SRC_DIR + 'graph_window.ui', self)
        self.go_back_btn_graph.clicked.connect(self.go_back_btn_fun)
        self.go_back_btn_graph_2.clicked.connect(self.build_plot)
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

    def build_plot(self):
        con = sqlite3.connect(DATABASE_DIR + 'Expenses_database.sqlite')
        cur = con.cursor()

        y_graph_list = list(map(lambda a: a[0], list(cur.execute("""SELECT * FROM expnstable;"""))))
        x_date_day = list(map(lambda a: a[2], list(cur.execute("""SELECT * FROM expnstable;"""))))
        x_date_mon = list(map(lambda a: a[3], list(cur.execute("""SELECT * FROM expnstable;"""))))
        x_date_year = list(map(lambda a: a[4], list(cur.execute("""SELECT * FROM expnstable;"""))))

        # self.graph_values - матрица, в которой хранятся два списка:
        # 1-ый содержит количество дней прошедших с начала добавления первого дохода & расхода
        # 2-ой содержит все расходы введённые пользователь на момент инициализации программы

        self.graph_values = [[int(list(x_date_day)[i]) - int(list(x_date_day)[0]) +
                              (self.month_days_from_start_of_year[int(list(x_date_mon)[i])])
                              - self.month_days_from_start_of_year[int(list(x_date_mon)[0])] +
                              (365 * (int(list(x_date_year)[i]) - int(list(x_date_year)[0])))
                              for i in range(len(list(x_date_day)))],
                             [sum(list(y_graph_list)[:j]) for j in range(len(list(y_graph_list)))]
                             ]
        self.graph_big.clear()
        self.graph_big.plot(self.graph_values[0], self.graph_values[1])
        con.close()

    def go_back_btn_fun(self) -> None:
        self.build_plot()
        self.hide()
