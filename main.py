from WorkWidgets.MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import sip

import sys


def main():

    app = QApplication([])
    main_window = MainWidget()

    main_window.setFixedSize(1300, 700)
    main_window.show()

    sys.exit(app.exec_())


main()
