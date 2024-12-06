from PyQt5.QtWidgets import QWidget, QVBoxLayout


def init_stock_prediction_tab(gui_main):
    stock_prediction_widget = QWidget()

    layout = QVBoxLayout()
    stock_prediction_widget.setLayout(layout)

    return stock_prediction_widget
