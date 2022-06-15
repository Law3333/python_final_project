from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json
from FunctionController import FunctionController
from PyQt5.QtWidgets import *
import sys
import os


class GetBookBasicInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("basic_info_widget")

        layout = QtWidgets.QVBoxLayout()

        header_laber = LabelComponent(18, "Get Book Basic Info")
        self.basic_info_widget = BasicInfoWidget()

        layout.addWidget(header_laber, stretch=1)
        layout.addWidget(self.basic_info_widget, stretch=9)
        self.setLayout(layout)

    def load(self):  # initial
        self.basic_info_widget.send_widget.reset_all_widgets()
        print("GetBookBasicInfoWidget & reset all widgets")


class BasicInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("basic_info_widget")

        layout = QtWidgets.QVBoxLayout()

        self.show_widget = ShowInfoWidget()
        show_scroll_area = QtWidgets.QScrollArea()
        show_scroll_area.setWidgetResizable(True)
        show_scroll_area.setWidget(self.show_widget)  # content
        show_scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.send_widget = SendInfoWidget(self.show_widget)

        layout.addWidget(self.send_widget, stretch=1)
        layout.addWidget(show_scroll_area, stretch=7)

        self.setLayout(layout)


class SendInfoWidget(QtWidgets.QWidget):
    def __init__(self, shower_callback):
        super().__init__()

        self.shower_callback = shower_callback
        self.cwd = os.getcwd()  # get currently file location

        layout = QtWidgets.QGridLayout()

        address_text_label = LabelComponent(14, "Address or Name : ")

        self.address_editor = LineEditComponent(
            "", 100, 250, 12)
        self.address_editor.mousePressEvent = self.clear_address_editor_content

        self.address_button = ButtonComponent("Address")
        self.address_button.clicked.connect(self.address_action)
        self.send_button = ButtonComponent("Send")
        self.send_button.clicked.connect(self.send_action)
        self.send_button.setEnabled(False)
        self.reset_button = ButtonComponent("Reset")
        self.reset_button.clicked.connect(self.reset_action)
        self.reset_button.setEnabled(False)

        layout.addWidget(address_text_label, 0, 0, 1, 1)
        layout.addWidget(self.address_editor, 0, 1, 1, 2)
        layout.addWidget(self.address_button, 1, 0, 1, 1)
        layout.addWidget(self.send_button, 1, 1, 1, 1)
        layout.addWidget(self.reset_button, 1, 2, 1, 1)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        self.setLayout(layout)

    def clear_address_editor_content(self, evnet):
        self.address_editor.clear()
        self.send_button.setEnabled(True)

    def address_action(self):
        print("address")
        self.filename_choose, self.filetype = QFileDialog.getOpenFileName(
            self, "Choose File", self.cwd, "CSV files (*.csv);;XML files (*.xml)"
        )

        if self.filename_choose == "":
            print("cancel")
        # print(self.filename_choose)
        # print(self.filetype)

        self.address_editor.setText(self.filename_choose)
        self.shower_callback.show_text_label.setText(self.filename_choose)
        self.send_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    '''------------------------------------------------------------------------------------------'''
    '''                                        Thread                                            '''

    def send_action(self):
        print("send action")
        # self.shower_callback.show_text_label.setText(
        #     "Execute Function\n123\n456\n\n\n\n\n\n\n789\n000")

        self.command = str()
        if ("csv" or "xml") in self.address_editor.text():
            self.command = "StoreData"
            print("address", self.address_editor.text())
        else:
            self.command = "SearchData"
            print("book_name", self.address_editor.text())

        self.show_command = FunctionController(
            self.address_editor.text(), self.command)
        self.show_command.start()
        self.show_command.return_sig.connect(self.show_process_result)

    def show_process_result(self, result):

        # result = list => [ book_name, author_info, book_barcode, book_request, location ]
        result = json.loads(result)

        show_items = ["書名    ", "作者    ", "條碼號", "索書號", "館藏地"]
        result_str = str()
        for result_info, items in zip(result, show_items):
            result_str += f"{items}  :   {result_info}\n"

        self.shower_callback.show_text_label.setText(result_str)
        self.reset_button.setEnabled(True)

    '''------------------------------------------------------------------------------------------'''

    def reset_action(self):
        print("reset action")
        self.reset_all_widgets()
        self.shower_callback.show_text_label.setText("Data reset")

    def reset_all_widgets(self):
        self.address_editor.setText(
            'Please Input "File Address" or "Book Name"')
        self.shower_callback.show_text_label.setText(" ")
        self.send_button.setEnabled(False)
        self.reset_button.setEnabled(False)


class ShowInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_scroll_area_widget")
        layout = QtWidgets.QVBoxLayout()

        self.show_text_label = LabelComponent(16, "", "left")

        layout.addWidget(self.show_text_label, stretch=1)

        self.setLayout(layout)
