import json

import matplotlib
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QWidget, QHBoxLayout, QToolTip
from matplotlib import ticker
from scipy.interpolate import interp1d

import stock_api
import GUI.gui_common

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from common import chinese_font


class ModelPageHszg(QWidget):

    model_id = 'hszg'
    model_name = '行业概念推导模型'
    model_description = '根据股票行业概念进行预测'
    def __init__(self, parent=None):
        super(ModelPageHszg, self).__init__(parent)
        self.gui_main = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
        edit = QtWidgets.QLineEdit()
        edit.textChanged.connect(lambda: self.search_hszg(edit.text()))
        edit.setPlaceholderText('Search By HSZG Code Or HSZG Name...')
        self.layout.addWidget(edit)
        self.table_widget = QTableWidget()
        self.table_widget.setFixedHeight(200)
        self.table_widget.setColumnCount(8)  # 设置列数

        # 设置表头标签
        self.table_widget.setHorizontalHeaderLabels(['name', 'code', 'type1', 'type2', 'level', 'pcode', 'pname', 'isleaf'])
        self.gui_main.stock_hszg = json.loads(stock_api.get_stock_hszg_list())
        self.table_widget.setRowCount(len(self.gui_main.stock_hszg))

        i = 0
        for item in self.gui_main.stock_hszg:
            # if item['code'] != 'chgn_700016':
            #     continue
            if item['isleaf'] == 0:
                continue
            self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(item['name']))
            self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(item['code']))
            self.table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.convert_type1(item['type1'])))
            self.table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem(self.convert_type2(item['type2'])))
            self.table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(item['level'])))
            self.table_widget.setItem(i, 5, QtWidgets.QTableWidgetItem(item['pcode']))
            self.table_widget.setItem(i, 6, QtWidgets.QTableWidgetItem(item['pname']))
            self.table_widget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(item['isleaf'])))
            i += 1
        self.table_widget.setRowCount(i)

        # 启用排序功能
        self.table_widget.setSortingEnabled(True)
        self.layout.addWidget(self.table_widget)
        self.table_widget.currentItemChanged.connect(lambda: self.switch_hszg(self.table_widget.currentItem()))

        self.layout.addWidget(GUI.gui_common.get_a_line(height=5))
        self.layout.addWidget(self.init_operation_area())
        self.layout.addWidget(GUI.gui_common.get_a_line(height=5))

        self.table_widget_stock = QTableWidget()
        self.table_widget_stock.setFixedHeight(400)
        self.table_widget_stock.setFixedWidth(600)
        self.table_widget_stock.setColumnCount(4)  # 设置列数
        self.table_widget_stock.setHorizontalHeaderLabels(['代码', '名称', '差异度0', '差异度1'])
        self.table_widget_stock.currentItemChanged.connect(lambda: self.switch_stock(self.table_widget_stock.currentItem()))
        # 启用排序功能
        self.table_widget_stock.setSortingEnabled(True)

        layout_bottom = QHBoxLayout()
        self.layout.addLayout(layout_bottom)
        layout_bottom.addWidget(self.table_widget_stock)
        # 创建 Matplotlib Canvas
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        layout_bottom.addWidget(self.canvas)
        # 绑定鼠标经过事件
        self.canvas.mpl_connect('motion_notify_event', self.on_canvas_motion_notify)
        self.canvas.mpl_connect('axes_leave_event', self.on_axes_leave)

    def convert_type1(self, type1):
        """
        一级分类（0:A股,1:创业板,2:科创板,3:基金,4:香港股市,5:债券,6:美国股市,7:外汇,8:期货,9:黄金,10:英国股市
        """
        convert_type1 = {
            0: 'A股',
            1: '创业板',
            2: '科创板',
            3: '基金',
            4: '香港股市',
            5: '债券',
            6: '美国股市',
            7: '外汇',
            8: '期货',
            9: '黄金',
            10: '英国股市'
        }
        return convert_type1.get(type1, '')

    def convert_type2(self, type2):
        """
        二级分类（0:A股-申万行业,1:A股-申万二级,2:A股-热门概念,3:A股-概念板块,4:A股-地域板块,5:A股-证监会行业,6:A股-分类,7:A股-指数成分,8:A股-风险警示,9:A股-大盘指数,10:A股-次新股,11:A股-沪港通,12:A股-深港通,13:基金-封闭式基金,14:基金-开放式基金,15:基金-货币型基金,16:基金-ETF基金净值,17:基金-ETF基金行情,18:基金-LOF基金行情,21:基金-科创板基金,22:香港股市-恒生行业,23:香港股市-全部港股,24:香港股市-热门港股,25:香港股市-蓝筹股,26:香港股市-红筹股,27:香港股市-国企股,28:香港股市-创业板,29:香港股市-指数,30:香港股市-A+H,31:香港股市-窝轮,32:香港股市-ADR,33:香港股市-沪港通,34:香港股市-深港通,35:香港股市-中华系列指数,36:债券-沪深债券,37:债券-深市债券,38:债券-沪市债券,39:债券-沪深可转债,40:美国股市-中国概念股,41:美国股市-科技类,42:美国股市-金融类,43:美国股市-制造零售类,44:美国股市-汽车能源类,45:美国股市-媒体类,46:美国股市-医药食品类,48:外汇-基本汇率,49:外汇-热门汇率,50:外汇-所有汇率,51:外汇-交叉盘汇率,52:外汇-美元相关汇率,53:外汇-人民币相关汇率,54:期货-全球期货,55:期货-中国金融期货交易所,56:期货-上海期货交易所,57:期货-大连商品交易所,58:期货-郑州商品交易所,59:黄金-黄金现货,60:黄金-黄金期货
        """
        convert_type2 = {
            0: '申万行业',
            1: '申万二级',
            2: '热门概念',
            3: '概念板块',
            4: '地域板块',
            5: '证监会行业',
            6: '分类',
            7: '指数成分',
            8: '风险警示',
            9: '大盘指数',
            10: '次新股',
            11: '沪港通',
            12: '深港通',
            13: '封闭式基金',
            14: '开放式基金',
            15: '货币型基金',
            16: 'ETF基金净值',
            17: 'ETF基金行情',
            18: 'LOF基金行情',
            21: '科创板基金',
            22: '恒生行业',
            23: '全部港股',
            24: '热门港股',
            25: '蓝筹股',
            26: '红筹股',
            27: '国企股',
            28: '创业板',
            29: '指数',
            30: 'A+H',
            31: '窝轮',
            32: 'ADR',
            33: '沪港通',
            34: '深港通',
            35: '中华系列指数',
            36: '沪深债券',
            37: '深市债券',
            38: '沪市债券',
            39: '沪深可转债',
            40: '中国概念股',
            41: '科技类',
            42: '金融类',
            43: '制造零售类',
            44: '汽车能源类',
            45: '媒体类',
            46: '医药食品类',
            48: '基本汇率',
            49: '热门汇率',
            50: '所有汇率',
            51: '交叉盘汇率',
            52: '美元相关汇率',
            53: '人民币相关汇率',
            54: '全球期货',
            55: '中国金融期货交易所',
            56: '上海期货交易所',
            57: '大连商品交易所',
            58: '郑州商品交易所',
            59: '黄金现货',
            60: '黄金期货'
        }
        return convert_type2.get(type2, '')

    def switch_hszg(self, it):
        hszg_code = self.table_widget.item(it.row(), 1).text()
        data = stock_api.get_stock_hszg_gg(hszg_code)
        if data == None or data == '':
            self.table_widget_stock.setRowCount(0)
            self.operation_area.setVisible(False)
            return
        self.hszg_gg = json.loads(data)
        print(self.hszg_gg)

        i = 0
        self.table_widget_stock.setRowCount(len(self.hszg_gg))
        for item in self.hszg_gg:
            if item['jys'] == None:
                continue
            self.table_widget_stock.setItem(i, 0, QtWidgets.QTableWidgetItem(item['dm']))
            self.table_widget_stock.setItem(i, 1, QtWidgets.QTableWidgetItem(item['mc']))
            self.table_widget_stock.setItem(i, 2, QtWidgets.QTableWidgetItem('-'))
            self.table_widget_stock.setItem(i, 3, QtWidgets.QTableWidgetItem('-'))
            i += 1
        self.table_widget_stock.setRowCount(i)
        self.operation_area.setVisible(self.table_widget_stock.rowCount() > 0)

    def search_hszg(self, text):
        if text == None:
            return
        if self.table_widget.rowCount() == 0:
            return

        for i in range(self.table_widget.rowCount()):
            if self.table_widget.item(i, 0).text().__contains__(text) or \
                    self.table_widget.item(i, 1).text().__contains__(text):
                self.table_widget.setRowHidden(i, False)
            else:
                self.table_widget.setRowHidden(i, True)

    def init_operation_area(self):
        self.operation_area = QtWidgets.QWidget()
        self.operation_area.setFixedHeight(50)
        layout = QHBoxLayout()
        self.operation_area.setLayout(layout)
        label = QtWidgets.QLabel('开始时间: ')
        label.setFixedWidth(80)
        label.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(label)
        editor = QtWidgets.QDateEdit(QtCore.QDate.fromString('2024-09-01', 'yyyy-MM-dd'))
        editor.setCalendarPopup(True)
        editor.setFixedWidth(140)
        editor.setDisplayFormat('yyyy-MM-dd')
        editor.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(editor)
        layout.addSpacing(20)
        label2 = QtWidgets.QLabel('结束时间: ')
        label2.setFixedWidth(80)
        label2.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(label2)
        editor2 = QtWidgets.QDateEdit(QtCore.QDate.fromString('2024-12-13', 'yyyy-MM-dd'))
        editor2.setCalendarPopup(True)
        editor2.setFixedWidth(140)
        editor2.setDisplayFormat('yyyy-MM-dd')
        editor2.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(editor2)
        button = QtWidgets.QPushButton('开始预测')
        button.setFixedWidth(100)
        button.setFont(QFont('Microsoft YaHei', 9))
        button.clicked.connect(lambda: self.start_prediction(editor.date().toString('yyyy-MM-dd'), editor2.date().toString('yyyy-MM-dd')))
        layout.addWidget(button)
        layout.addStretch()
        self.tooltip_label = QtWidgets.QLabel()
        self.tooltip_label.setFixedWidth(200)
        self.tooltip_label.setFont(QFont('Microsoft YaHei', 9))
        layout.addWidget(self.tooltip_label)
        self.operation_area.setVisible(False)
        return self.operation_area

    def start_prediction(self, start_date, end_date):
        if self.table_widget_stock.rowCount() == 0 or\
                self.hszg_gg == None or\
                len(self.hszg_gg) == 0:
            return

        self.start_date = start_date
        self.end_date = end_date

        # 行业概念的数据：日期对该日涨跌幅
        hszg_date2zd = {}

        for item in self.hszg_gg:
            data = stock_api.get_stock_fsjj_info(item['dm'], 'dn', start_date, end_date)
            if data == None:
                continue
            jysj = json.loads(data)
            if len(jysj) == 0:
                continue
            for entry in jysj:
                date = entry['d']
                zd = [entry['zd']]
                if date not in hszg_date2zd:
                    hszg_date2zd[date] = zd
                else:
                    hszg_date2zd[date].append(zd[0])


        self.dates = []
        self.zds = []
        for date in hszg_date2zd:
            self.dates.append(date)
            self.zds.append(sum(hszg_date2zd[date]) / len(hszg_date2zd[date]))

        # 将日期转换为数值类型
        date_nums = [matplotlib.dates.datestr2num(date) for date in self.dates]

        # 使用样条插值生成更多数据点
        f = interp1d(date_nums, self.zds, kind='cubic')
        new_date_nums = np.linspace(min(date_nums), max(date_nums), 300)
        new_close_prices = f(new_date_nums)
        # 清除之前的图形
        fig = self.canvas.figure
        fig.clear()

        # 绘制曲线图
        ax = fig.add_subplot(111)
        ax.plot(matplotlib.dates.num2date(date_nums), self.zds, label='涨跌幅')

        ax.set_xlabel('日期', fontproperties=chinese_font)
        ax.set_ylabel('涨跌幅', fontproperties=chinese_font)
        ax.set_title(f'{self.table_widget.item(self.table_widget.currentItem().row(), 0).text()} 涨跌幅曲线图', fontproperties=chinese_font)
        ax.legend(prop=chinese_font)  # 指定图例字体

        # 旋转日期标签、设置刻度间隔
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # 只显示10个主要刻度
        ax.xaxis.set_tick_params(rotation=45)

        # 自动调整日期标签
        fig.autofmt_xdate()

        # 更新 Canvas
        self.canvas.draw()

        # 计算数据差异度
        similarity = {}
        similarity_1 = {}
        for item in self.hszg_gg:
            data = stock_api.get_stock_fsjj_info(item['dm'], 'dn', start_date, end_date)
            if data == None:
                continue
            jysj = json.loads(data)
            if len(jysj) == 0:
                continue
            stocd_to_hszg_similarity = []
            stocd_to_hszg_similarity_1 = []
            for i in range(len(jysj) - 1):
                entry = jysj[i]
                entry_1 = jysj[i + 1]
                date = entry['d']
                value_hszg = sum(hszg_date2zd[date]) / len(hszg_date2zd[date]) + 10
                value_stock = entry['zd'] + 10
                value_stock_1 = entry_1['zd'] + 10
                stocd_to_hszg_similarity.append(abs(value_stock - value_hszg) * 100 / value_hszg)
                stocd_to_hszg_similarity_1.append(abs(value_stock_1 - value_hszg) * 100 / value_hszg)

            similarity[item['dm']] = sum(stocd_to_hszg_similarity) / len(stocd_to_hszg_similarity)
            similarity_1[item['dm']] = sum(stocd_to_hszg_similarity_1) / len(stocd_to_hszg_similarity_1)

        # 更新code表格
        for i in range(self.table_widget_stock.rowCount()):
            code = self.table_widget_stock.item(i, 0).text()
            if code in similarity:
                self.table_widget_stock.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{similarity[code]:.2f}"))
            if code in similarity_1:
                self.table_widget_stock.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{similarity_1[code]:.2f}"))



    def switch_stock(self, it):
        if not hasattr(self, 'start_date'):
            return
        stock_code = self.table_widget_stock.item(it.row(), 0).text()
        print(f"切换到股票代码：{stock_code}")
        data = stock_api.get_stock_fsjj_info(stock_code, 'dn', self.start_date, self.end_date)
        if data == None:
            return
        jysj = json.loads(data)
        if len(jysj) == 0:
            return
        stock_zds = []
        stock_dates = []
        for entry in jysj:
            stock_dates.append(entry['d'])
            stock_zds.append(entry['zd'])

        # 将日期转换为数值类型
        date_nums = [matplotlib.dates.datestr2num(date) for date in self.dates]
        date_nums2 = [matplotlib.dates.datestr2num(date) for date in stock_dates]

        # 使用样条插值生成更多数据点
        f = interp1d(date_nums, self.zds, kind='cubic')
        new_date_nums = np.linspace(min(date_nums), max(date_nums), 300)
        new_zds = f(new_date_nums)

        f2 = interp1d(date_nums2, stock_zds, kind='cubic')
        new_date_nums2 = np.linspace(min(date_nums2), max(date_nums2), 300)
        new_stock_zds = f2(new_date_nums2)
        # 清除之前的图形
        fig = self.canvas.figure
        fig.clear()

        # 绘制曲线图
        ax = fig.add_subplot(111)
        ax.plot(matplotlib.dates.num2date(date_nums), self.zds, label='涨跌幅')
        # 绘制第二条曲线
        ax.plot(matplotlib.dates.num2date(date_nums2), stock_zds, label=f'{self.table_widget_stock.item(self.table_widget_stock.currentItem().row(), 1).text()}', color='red')
        ax.set_xlabel('日期', fontproperties=chinese_font)
        ax.set_ylabel('涨跌幅', fontproperties=chinese_font)
        ax.set_title(f'{self.table_widget.item(self.table_widget.currentItem().row(), 0).text()} 涨跌幅曲线图',
                     fontproperties=chinese_font)
        ax.legend(prop=chinese_font)  # 指定图例字体

        # 旋转日期标签、设置刻度间隔
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # 只显示10个主要刻度
        ax.xaxis.set_tick_params(rotation=45)

        # 自动调整日期标签
        fig.autofmt_xdate()

        # 更新 Canvas
        self.canvas.draw()

    def on_canvas_motion_notify(self, event):
        # 处理鼠标点击事件
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            # 将 x 转换为日期对象
            date_obj = matplotlib.dates.num2date(x)
            # 提取日期部分
            date_str = date_obj.date().strftime('%Y-%m-%d')
            self.tooltip_label.setText(f"{date_str}：{y:.2f}%")

            tooltip_text = f"{date_str}, {y:.2f}%"

            # 手动显示工具提示
            QToolTip.showText(event.guiEvent.globalPos(), tooltip_text, self.canvas)

    def on_axes_leave(self, event):
        self.tooltip_label.setText('')