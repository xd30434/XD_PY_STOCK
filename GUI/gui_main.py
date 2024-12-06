import json
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget, QVBoxLayout, QListWidget, QTabWidget, \
    QTableWidget, QHBoxLayout, QScrollArea, QAction, QMessageBox

import stock_api
from GUI.gui_tab_stock_info import init_stock_info_tab
from GUI.gui_tab_stock_prediction import init_stock_prediction_tab
from GUI.gui_tab_stock_simulation import init_stock_simulation_tab


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('XD_STOCK')

        # 自动适应屏幕宽高
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(QtCore.QRect(0, 0, screen.width(), screen.height()))
        self.showMaximized()

        # 设置QTabWidget为中心窗口部件
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # self.stock_hs_list = None

        self.stock_info_widget, self.stock_info_table_widget, self.layout_detail = init_stock_info_tab(self)
        self.tab_widget.addTab(self.stock_info_widget, 'Stock Info')

        self.stock_prediction_widget = init_stock_prediction_tab(self)
        self.tab_widget.addTab(self.stock_prediction_widget, 'Stock Prediction')

        self.stock_simulation_widget = init_stock_simulation_tab(self)
        self.tab_widget.addTab(self.stock_simulation_widget, 'Stock Simulation')

        # 添加菜单栏
        self.create_menu_bar()

    def create_menu_bar(self):
        # 创建菜单栏
        menu_bar = self.menuBar()

        # 添加文件菜单
        file_menu = menu_bar.addMenu('文件')

        # 添加打开文件操作
        open_action = QAction('打开文件', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('打开文件')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # 添加保存文件操作
        save_action = QAction('保存文件', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('保存文件')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # 添加退出操作
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用程序')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 添加帮助菜单
        help_menu = menu_bar.addMenu('帮助')

        # 添加关于操作
        about_action = QAction('关于', self)
        about_action.setStatusTip('关于应用程序')
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def open_file(self):
        # 实现打开文件的逻辑
        print("打开文件")

    def save_file(self):
        # 实现保存文件的逻辑
        print("保存文件")

    def show_about_dialog(self):
        # 显示关于对话框
        QMessageBox.about(self, '关于 XD_STOCK', '这是一个股票分析应用程序。')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建并显示全屏窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())
