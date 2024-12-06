import json

import matplotlib
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from matplotlib import ticker
from scipy.interpolate import interp1d
import stock_api

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from common import chinese_font


def init_stock_simulation_tab(gui_main):
    stock_simulation_widget = QWidget()
    layout = QHBoxLayout()
    stock_simulation_widget.setLayout(layout)
    widget_left = QWidget()
    layout.addWidget(widget_left)
    widget_left.setFixedWidth(500)
    layout_left = QVBoxLayout()
    widget_left.setLayout(layout_left)

    widget_right = QWidget()
    layout_right = QVBoxLayout()
    widget_right.setLayout(layout_right)
    layout.addWidget(widget_right)

    # 1. 输入股票代码
    hl1, editor_stock_code = new_line('股票代码:', '', 'edit')
    layout_left.addLayout(hl1)
    # 2. 输入购买数量
    hl2, editor_buy_num = new_line('买入数量(手):', '10', 'edit')
    layout_left.addLayout(hl2)
    editor_buy_num.setValidator(QtGui.QIntValidator())
    # 3. 输入买入日期
    hl3, editor_buy_date = new_line('买入日期:', QtCore.QDate.currentDate().addMonths(-1).toString('yyyy-MM-dd'), 'date')
    layout_left.addLayout(hl3)
    # 4. 输入卖出日期
    hl4, editor_sell_date = new_line('卖出日期:', QtCore.QDate.currentDate().toString('yyyy-MM-dd'), 'date')
    layout_left.addLayout(hl4)
    # 5. 开始模拟
    start_button = QtWidgets.QPushButton('开始模拟')
    start_button.setFixedWidth(459)
    layout_left.addWidget(start_button)
    # 6. 结果展示区
    layout_simulation_result = QVBoxLayout()
    layout_left.addLayout(layout_simulation_result)
    start_button.clicked.connect(lambda: start_simulation(gui_main, layout_simulation_result, editor_stock_code.text(), float(editor_buy_num.text()) * 100, editor_buy_date.text(), editor_sell_date.text()))
    layout_simulation_result.addStretch()

    # 创建 Matplotlib Canvas
    fig = Figure()
    canvas = FigureCanvas(fig)
    layout_right.addWidget(canvas)

    # 添加工具栏
    toolbar = NavigationToolbar(canvas, stock_simulation_widget)
    layout_right.addWidget(toolbar)

    return stock_simulation_widget

def start_simulation(gui_main, layout, stock_code, buy_num, buy_date, sell_date):
    data = stock_api.get_stock_company_introduction(stock_code)
    print(data)
    if data == None:
        return
    gsjj = json.loads(data)

    while layout.count():
        it = layout.takeAt(0)
        layout.removeItem(it)

    for item in gui_main.stock_hs_list:
        if item['dm'] == stock_code:
            layout.addLayout(new_line('股票代码:', stock_code, 'text')[0])
            layout.addLayout(new_line('公司简称:', item['mc'], 'text')[0])
            break

    data = stock_api.get_stock_fsjj_info(stock_code, 'dn', buy_date, sell_date)
    if data == None:
        return
    print(data)
    jysj = json.loads(data)
    if len(jysj) > 0:
        # 获取日期和收盘价数据
        dates = [entry['d'] for entry in jysj]
        close_prices = [entry['c'] for entry in jysj]

        # 将日期转换为数值类型
        date_nums = [matplotlib.dates.datestr2num(date) for date in dates]

        # 使用样条插值生成更多数据点
        f = interp1d(date_nums, close_prices, kind='cubic')
        new_date_nums = np.linspace(min(date_nums), max(date_nums), 300)
        new_close_prices = f(new_date_nums)
        # 清除之前的图形
        fig = layout.parentWidget().parentWidget().findChild(FigureCanvas).figure
        fig.clear()

        # 绘制曲线图
        ax = fig.add_subplot(111)
        ax.plot(matplotlib.dates.num2date(new_date_nums), new_close_prices, label='收盘价')
        ax.set_xlabel('日期', fontproperties=chinese_font)
        ax.set_ylabel('收盘价', fontproperties=chinese_font)
        ax.set_title(f'{gsjj['name']} 股票收盘价曲线图', fontproperties=chinese_font)
        ax.legend(prop=chinese_font)  # 指定图例字体

        # 旋转日期标签、设置刻度间隔
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # 只显示10个主要刻度
        ax.xaxis.set_tick_params(rotation=45)

        # 自动调整日期标签
        fig.autofmt_xdate()

        # 更新 Canvas
        layout.parentWidget().parentWidget().findChild(FigureCanvas).draw()

        layout.addLayout(new_line('公司全称:', gsjj['name'], 'text')[0])
        layout.addLayout(new_line('买入单价:', str(jysj[0]['o']), 'text')[0])
        layout.addLayout(new_line('卖出单价:', str(jysj[-1]['c']), 'text')[0])
        layout.addLayout(new_line('买入总金额:', str(jysj[0]['o'] * buy_num), 'text')[0])
        layout.addLayout(new_line('卖出总金额:', str(jysj[-1]['c'] * buy_num), 'text')[0])
        layout.addLayout(new_line('收益金额:', str((jysj[-1]['c'] - jysj[0]['o']) * buy_num), 'text')[0])
        layout.addLayout(new_line('收益率:', str((jysj[-1]['c'] - jysj[0]['o']) / jysj[0]['o'] * 100) + '%', 'text')[0])

    layout.addStretch()

def stock_code_edit_changed(controller):
    """
    当股票代码编辑框的文本发生变化时调用此函数。
    """
    try:
        text = controller.text()

        # 检查是否为空字符串
        if not text:
            # 处理空字符串的情况
            return

        # 检查是否包含非字母数字字符
        if not text.isalnum():
            # 处理包含非字母数字字符的情况
            return

        # 执行原有的逻辑代码
        process_stock_code(text)
    except Exception as e:
        print(f"Error in stock_code_edit_changed: {e}")

def process_stock_code(self, text):
    """
    处理股票代码的逻辑。
    """
    # 原有的逻辑代码
    pass

def new_line(text, content, type):
    layout = QHBoxLayout()
    label = QtWidgets.QLabel(text)
    label.setFixedWidth(120)
    layout.addWidget(label)
    if type == 'text':
        editor = QtWidgets.QLineEdit(content)
        editor.setReadOnly(True)
        editor.setFixedWidth(300)
        layout.addWidget(editor)
    elif type == 'edit':
        editor = QtWidgets.QLineEdit(content)
        editor.setFixedWidth(300)
        layout.addWidget(editor)
    elif type == 'date':
        editor = QtWidgets.QDateEdit(QtCore.QDate.fromString(content, 'yyyy-MM-dd'))
        editor.setCalendarPopup(True)
        editor.setFixedWidth(300)
        editor.setDisplayFormat('yyyy-MM-dd')
        layout.addWidget(editor)
    else:
        editor = QtWidgets.QTextEdit(content)
        editor.setFixedWidth(300)
        editor.setReadOnly(True)
        layout.addWidget(editor)

    return layout, editor