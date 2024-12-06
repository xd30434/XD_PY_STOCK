import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QScrollArea

import stock_api


def init_stock_info_tab(gui_main):
    # 创建一个QWidget作为中心窗口部件
    stock_info_widget = QWidget()

    layout = QHBoxLayout()
    stock_info_widget.setLayout(layout)

    # 创建一个QVBoxLayout来管理布局
    layout_left = QVBoxLayout()
    layout.addLayout(layout_left)

    edit = QtWidgets.QLineEdit()
    edit.textChanged.connect(lambda: search_stock(gui_main, edit.text()))
    edit.setPlaceholderText('Search By Stock Code Or Stock Name...')
    layout_left.addWidget(edit)

    # 创建一个QTableWidget
    table_widget = QTableWidget()
    table_widget.setColumnCount(3)  # 设置列数

    # 设置表头标签
    table_widget.setHorizontalHeaderLabels(['Stock Code', 'Stock Name', 'Stock Exchange'])
    gui_main.stock_hs_list = json.loads(stock_api.get_stock_hs_list())

    i = 0
    table_widget.setRowCount(len(gui_main.stock_hs_list))
    for item in gui_main.stock_hs_list:
        table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(item['dm']))
        table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(item['mc']))
        table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(item['jys']))
        i += 1

    table_widget.currentItemChanged.connect(lambda: show_stock_company_info(gui_main, table_widget.currentItem()))

    # 将QListWidget添加到布局中
    layout_left.addWidget(table_widget)

    layout_right = QVBoxLayout()
    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)
    layout_right.addWidget(scrollArea)

    layout.addLayout(layout_right)
    layout_detail = QVBoxLayout()
    scrollArea.setLayout(layout_detail)

    return stock_info_widget, table_widget, layout_detail


def search_stock(gui_main, text):
    if text == None:
        return
    if gui_main.stock_info_table_widget.rowCount() == 0:
        return

    for i in range(gui_main.stock_info_table_widget.rowCount()):
        if gui_main.stock_info_table_widget.item(i, 0).text().__contains__(text) or \
                gui_main.stock_info_table_widget.item(i, 1).text().__contains__(text):
            gui_main.stock_info_table_widget.setRowHidden(i, False)
        else:
            gui_main.stock_info_table_widget.setRowHidden(i, True)


def show_stock_company_info(gui_main, item):
    if item == None:
        return
    while gui_main.layout_detail.count():
        it = gui_main.layout_detail.takeAt(0)
        gui_main.layout_detail.removeItem(it)

    gsjj = stock_api.get_stock_company_introduction(gui_main.stock_info_table_widget.item(item.row(), 0).text())
    print(gsjj)
    data = json.loads(gsjj)
    gui_main.layout_detail.addLayout(new_line('名称:', data['name'], 'text'))
    gui_main.layout_detail.addLayout(new_line('英文名称:', data['ename'], 'text'))
    gui_main.layout_detail.addLayout(new_line('交易所:', data['market'], 'text'))
    gui_main.layout_detail.addLayout(new_line('成立日期:', data['rdate'], 'text'))
    gui_main.layout_detail.addLayout(new_line('上市日期:', data['ldate'], 'text'))
    gui_main.layout_detail.addLayout(new_line('发行价格(元):', data['sprice'], 'text'))
    gui_main.layout_detail.addLayout(new_line('主承销商:', data['principal'], 'text'))
    gui_main.layout_detail.addLayout(new_line('注册资本:', data['rprice'], 'text'))
    gui_main.layout_detail.addLayout(new_line('机构类型:', data['instype'], 'text'))
    gui_main.layout_detail.addLayout(new_line('组织形式:', data['organ'], 'text'))
    gui_main.layout_detail.addLayout(new_line('董事会秘书:', data['secre'], 'text'))
    gui_main.layout_detail.addLayout(new_line('公司网站:', data['site'], 'text'))
    gui_main.layout_detail.addLayout(new_line('注册地址:', data['addr'], 'text'))
    gui_main.layout_detail.addLayout(new_line('办公地址:', data['oaddr'], 'text'))
    gui_main.layout_detail.addLayout(new_line('公司简介:', data['desc'], 'text2'))
    gui_main.layout_detail.addLayout(new_line('经营范围:', data['bscope'], 'text2'))
    gui_main.layout_detail.addLayout(new_line('概念及板块:', data['idea'], 'text'))
    gui_main.layout_detail.addLayout(new_line('承销方式:', data['printype'], 'text'))
    gui_main.layout_detail.addLayout(new_line('上市推荐人:', data['referrer'], 'text'))
    gui_main.layout_detail.addLayout(new_line('发行方式:', data['putype'], 'text'))
    gui_main.layout_detail.addLayout(new_line('发行市盈率:', data['pe'], 'text'))

    # 添加一个占位符
    # self.layout_detail.addStretch()


def new_line(text, content, type):
    layout = QHBoxLayout()
    label = QtWidgets.QLabel(text)
    label.setFixedWidth(120)
    layout.addWidget(label)
    if type == 'text':
        text_edit = QtWidgets.QLineEdit(content)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
    else:
        text_edit = QtWidgets.QTextEdit(content)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

    return layout

