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
        widget = it.widget()
        if widget:
            widget.deleteLater()
        gui_main.layout_detail.removeItem(it)

    data = stock_api.get_stock_company_introduction(gui_main.stock_info_table_widget.item(item.row(), 0).text())
    if data == None:
        return
    gsjj = json.loads(data)
    gui_main.layout_detail.addLayout(new_line('名称:', gsjj['name'], 'text', 'obj_name_name'))
    gui_main.layout_detail.addLayout(new_line('英文名称:', gsjj['ename'], 'text', 'obj_name_ename'))
    gui_main.layout_detail.addLayout(new_line('交易所:', gsjj['market'], 'text', 'obj_name_market'))
    gui_main.layout_detail.addLayout(new_line('成立日期:', gsjj['rdate'], 'text', 'obj_name_rdate'))
    gui_main.layout_detail.addLayout(new_line('上市日期:', gsjj['ldate'], 'text', 'obj_name_ldate'))
    gui_main.layout_detail.addLayout(new_line('发行价格(元):', gsjj['sprice'], 'text', 'obj_name_sprice'))
    gui_main.layout_detail.addLayout(new_line('主承销商:', gsjj['principal'], 'text', 'obj_name_principal'))
    gui_main.layout_detail.addLayout(new_line('注册资本:', gsjj['rprice'], 'text', 'obj_name_rprice'))
    gui_main.layout_detail.addLayout(new_line('机构类型:', gsjj['instype'], 'text', 'obj_name_instype'))
    gui_main.layout_detail.addLayout(new_line('组织形式:', gsjj['organ'], 'text', 'obj_name_organ'))
    gui_main.layout_detail.addLayout(new_line('董事会秘书:', gsjj['secre'], 'text', 'obj_name_secre'))
    gui_main.layout_detail.addLayout(new_line('公司网站:', gsjj['site'], 'text', 'obj_name_site'))
    gui_main.layout_detail.addLayout(new_line('注册地址:', gsjj['addr'], 'text', 'obj_name_addr'))
    gui_main.layout_detail.addLayout(new_line('办公地址:', gsjj['oaddr'], 'text', 'obj_name_oaddr'))
    gui_main.layout_detail.addLayout(new_line('公司简介:', gsjj['desc'], 'text2', 'obj_name_desc'))
    gui_main.layout_detail.addLayout(new_line('经营范围:', gsjj['bscope'], 'text2', 'obj_name_bscope'))
    gui_main.layout_detail.addLayout(new_line('概念及板块:', gsjj['idea'], 'text2', 'obj_name_idea'))
    gui_main.layout_detail.addLayout(new_line('承销方式:', gsjj['printype'], 'text', 'obj_name_printype'))
    gui_main.layout_detail.addLayout(new_line('上市推荐人:', gsjj['referrer'], 'text', 'obj_name_referrer'))
    gui_main.layout_detail.addLayout(new_line('发行方式:', gsjj['putype'], 'text', 'obj_name_putype'))
    gui_main.layout_detail.addLayout(new_line('发行市盈率:', gsjj['pe'], 'text', 'obj_name_pe'))

    # 添加一个占位符
    # self.layout_detail.addStretch()


def new_line(text, content, type, obj_name):
    layout = QHBoxLayout()
    layout.setObjectName(obj_name)
    label = QtWidgets.QLabel(text)
    label.setFixedWidth(120)
    layout.addWidget(label)
    if type == 'text':
        text_edit = QtWidgets.QLineEdit(content)
        text_edit.setReadOnly(True)
        text_edit.setObjectName(obj_name + '1')
        layout.addWidget(text_edit)
    else:
        text_edit = QtWidgets.QTextEdit(content)
        text_edit.setReadOnly(True)
        text_edit.setObjectName(obj_name)
        layout.addWidget(text_edit)

    return layout

