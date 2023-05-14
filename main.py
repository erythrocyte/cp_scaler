import sys
from PyQt5 import QtWidgets

from gui.main_view import MainView
# from bin import run


def main():
    app = QtWidgets.QApplication(sys.argv)
    v = MainView()
    v.show()
    sys.exit(app.exec_())

    # run.do()


if __name__ == '__main__':
    main()
