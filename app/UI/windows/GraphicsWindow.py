
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.methods.db_queries import get_rows
from app.methods.matrix_tools import transpose
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
        if data := transpose(get_rows(0)):
            y_graph_list = data[1]
            x_date_day = map(lambda x: x[x.rfind('-') + 1:], data[-1])
            x_date_mon = map(lambda x: x[x.find('-') + 1: x.rfind('-')], data[-1])
            x_date_year = map(lambda x: x[: x.find('-')], data[-1])
            print(x_date_day, x_date_mon, x_date_year, sep="\n\n")
            # self.graph_values - матрица, в которой хранятся два списка:
            # 1-ый содержит количество дней прошедших с начала добавления первого дохода \ расхода
            # 2-ой содержит все расходы введённые пользователь на момент инициализации программы

            print(list(x_date_day))
            self.graph_values = [[list(x_date_day)[i] +
                                  self.month_days_from_start_of_year[list(x_date_mon)[i]] +
                                  (365 * list(x_date_year)[i]) -
                                  list(x_date_day)[0] +
                                  self.month_days_from_start_of_year[list(x_date_mon)[0]] +
                                  (365 * list(x_date_year)[0])
                                  for i in range(len(list(x_date_day)))],
                                 list(y_graph_list)
                                 ]

            self.graph_big.clear()
            self.graph_big.plot(self.graph_values[0], self.graph_values[1])

    def go_back_btn_fun(self) -> None:
        self.build_plot()
        self.hide()
