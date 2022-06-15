from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.Get_Book_Basic_Info_Widgets import GetBookBasicInfoWidget
from WorkWidgets.Get_Book_image_Widgets import GetBookImageWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")

        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # self.setStyleSheet(
        #     """
        #         QWidget#main_widget{{
        #             color: white;
        #             border-image: url(\"{}\");
        #         }};
        #     """.format("./Image/base.jpg")
        # )

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(22, "NTUT Library Manager")
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(menu_widget, 1, 0, 1, 1)
        layout.addWidget(function_widget, 1, 1, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 10)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 7)

        self.setLayout(layout)


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QVBoxLayout()

        info_button = ButtonComponent("Basic Info")
        image_button = ButtonComponent("Book Image")

        info_button.clicked.connect(
            lambda: self.update_widget_callback("BasicInfo"))
        image_button.clicked.connect(
            lambda: self.update_widget_callback("BookImage"))

        layout.addWidget(info_button, stretch=1)
        layout.addWidget(image_button, stretch=1)

        self.setLayout(layout)


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "BasicInfo": self.addWidget(GetBookBasicInfoWidget()),
            "BookImage": self.addWidget(GetBookImageWidget())
        }
        self.update_widget("BasicInfo")

    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()
