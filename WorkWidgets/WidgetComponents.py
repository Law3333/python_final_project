from PyQt5 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, align='center', color='black'):
        super().__init__()

        align_action = {
            "center": QtCore.Qt.AlignCenter,
            "left": QtCore.Qt.AlignLeft
        }
        self.setWordWrap(True)  # 自動換行
        self.setAlignment(align_action[align])  # 靠左對齊
        # self.setAlignment(QtCore.Qt.AlignCenter)  # 置中
        self.setStyleSheet(f"color:{color}")

        self.setFont(QtGui.QFont("微軟正黑體", font_size, QtGui.QFont.Bold))
        self.setText(content)  # 把內容秀出來


class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=20, width=250, font_size=16):
        super().__init__()
        self.setMaxLength(length)  # 字串長度
        self.setText(default_content)  # 這邊default_content 為 name
        # self.setMinimumHeight(30)  # 高度
        # self.setMaximumWidth(width)  # 框框的長度
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0);border:2px groove gray;border-radius:10px;padding:2px 4px")


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()

        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet(
            'border:2px groove gray;border-radius:10px;padding:2px 4px;')
        self.setFlat(True)
