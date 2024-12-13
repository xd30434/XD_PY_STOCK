from PyQt5.QtWidgets import QFrame


def get_a_line(type = QFrame.HLine, height = 1):
    line = QFrame()
    line.setFrameShape(type)  # 设置为垂直线
    line.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
    line.setFixedHeight(height)
    return line