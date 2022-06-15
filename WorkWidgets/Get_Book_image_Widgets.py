from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json


class GetBookImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("book_image_widget")

        layout = QtWidgets.QVBoxLayout()

        header_laber = LabelComponent(18, "Get Book image")
        self.modify_widget = BookImageWidget()

        layout.addWidget(header_laber, stretch=1)
        layout.addWidget(self.modify_widget, stretch=9)
        self.setLayout(layout)

    def load(self):  # initial

        print("GetBookImageWidget")


class BookImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("book_image_widget")

        layout = QtWidgets.QHBoxLayout()


        self.setLayout(layout)
