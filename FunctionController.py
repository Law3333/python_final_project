from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import json
from Function.crawler_info import *
from Function.crawler_photo import *


class FunctionController(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, info_data, command):
        super().__init__()
        self.command = command
        self.crawler_info = get_basic_info(info_data)
        self.crawler_photo = get_photo(info_data)

    def run(self):
        if self.command == "SearchData":

            book_name, author_info, book_barcode, book_request, location = self.crawler_info.get_basic_info()
            result = [book_name, author_info,
                      book_barcode, book_request, location]
            self.return_sig.emit(json.dumps(result))
