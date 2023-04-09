import sys
import logging
from PyQt5 import QtWidgets, QtCore

from gui.main_view import MainView


def main():
    app = QtWidgets.QApplication(sys.argv)
    v = MainView()
    v.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
