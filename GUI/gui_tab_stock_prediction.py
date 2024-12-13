from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFrame, QTabWidget

import GUI.gui_common
from GUI.model_page.model_page_hszg import ModelPageHszg
from GUI.model_page.model_page_dp import ModelPageDP
from GUI.model_page.model_page_stock_to_hszg import ModelPagestockToHszg

model_list = [ModelPageHszg, ModelPageDP, ModelPagestockToHszg]

def init_stock_prediction_tab(gui_main):
    stock_prediction_widget = QWidget()

    layout = QVBoxLayout()
    stock_prediction_widget.setLayout(layout)
    layout_model_selector = QHBoxLayout()
    layout.addLayout(layout_model_selector)
    layout_model_selector.addWidget(QLabel('模型选择:'))
    combo_box_model_selector = QComboBox()
    for model in model_list:
        combo_box_model_selector.addItem(model.model_name, model.model_id)
    combo_box_model_selector.setFixedWidth(500)
    layout_model_selector.addWidget(combo_box_model_selector)
    layout_model_selector.addStretch()
    combo_box_model_selector.currentIndexChanged.connect(lambda: switch_model_page(gui_main, combo_box_model_selector.currentIndex()))
    layout.addWidget(GUI.gui_common.get_a_line())

    gui_main.tab_model_page = QTabWidget()
    layout.addWidget(gui_main.tab_model_page)

    for i in range(len(model_list)):
        gui_main.tab_model_page.addTab(model_list[i](gui_main), model_list[i].model_name)
    gui_main.tab_model_page.tabBar().setVisible(False)
    layout.addStretch()



    return stock_prediction_widget

def switch_model_page(gui_main, index):
    gui_main.tab_model_page.setCurrentIndex(index)