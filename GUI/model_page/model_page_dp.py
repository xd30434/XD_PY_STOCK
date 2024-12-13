import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QTreeWidget, QTableWidget, QWidget, QVBoxLayout

import GUI.gui_common
import stock_api


class ModelPageDP(QWidget):

    model_id = 'dp'
    model_name = '大盘推导模型'
    model_description = '根据股票大盘进行预测'

    def __init__(self, parent=None):
        super(ModelPageDP, self).__init__(parent)
        self.gui_main = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
        table_widget = QTableWidget()
        table_widget.setFixedHeight(400)
        table_widget.setColumnCount(8)  # 设置列数

        # 设置表头标签
        table_widget.setHorizontalHeaderLabels(['name', 'code', 'type1', 'type2', 'level', 'pcode', 'pname', 'isleaf'])
        self.gui_main.stock_hszg = json.loads(stock_api.get_stock_hszg_list())

        i = 0
        table_widget.setRowCount(len(self.gui_main.stock_hszg))
        for item in self.gui_main.stock_hszg:
            table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(item['name']))
            table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(item['code']))
            table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.convert_type1(item['type1'])))
            table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem(self.convert_type2(item['type2'])))
            table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(item['level'])))
            table_widget.setItem(i, 5, QtWidgets.QTableWidgetItem(item['pcode']))
            table_widget.setItem(i, 6, QtWidgets.QTableWidgetItem(item['pname']))
            table_widget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(item['isleaf'])))
            i += 1
        self.layout.addWidget(table_widget)

        self.layout.addWidget(GUI.gui_common.get_a_line(height=30))

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
