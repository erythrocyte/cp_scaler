from PyQt5 import QtWidgets, QtCore


class UiWellIntersectView:
    set_progress = QtCore.pyqtSignal(int)

    def __init__(self):
        self.btn_run = QtWidgets.QPushButton()
        self.data_fn = QtWidgets.QLineEdit()
        self.btn_data_fn = None
        self.well_track_fn = QtWidgets.QLineEdit()
        self.btn_wt_fn = None
        self.result_fn = QtWidgets.QLineEdit()
        self.btn_result_fn = None

    def setup_ui(self, widget: QtWidgets.QWidget):
        self.__createComponents(widget)

    def __createComponents(self, widget: QtWidgets.QWidget):
        l = QtWidgets.QGridLayout()

        # data
        lbl = QtWidgets.QLabel("DATA file")
        l.addWidget(lbl, 0, 0, 1, 1)
        self.data_fn = QtWidgets.QLineEdit()
        l.addWidget(self.data_fn, 0, 1, 1, 4)
        self.btn_data_fn = QtWidgets.QPushButton("...")
        l.addWidget(self.btn_data_fn, 0, 5, 1, 1)

        # well track
        lbl = QtWidgets.QLabel("Well track file")
        l.addWidget(lbl, 1, 0, 1, 1)
        self.well_track_fn = QtWidgets.QLineEdit()
        l.addWidget(self.well_track_fn, 1, 1, 1, 4)
        self.btn_wt_fn = QtWidgets.QPushButton("...")
        l.addWidget(self.btn_wt_fn, 1, 5, 1, 1)

        # result file
        lbl = QtWidgets.QLabel("Result file")
        l.addWidget(lbl, 2, 0, 1, 1)
        self.result_fn = QtWidgets.QLineEdit()
        l.addWidget(self.result_fn, 2, 1, 1, 4)
        self.btn_result_fn = QtWidgets.QPushButton("...")
        l.addWidget(self.btn_result_fn, 2, 5, 1, 1)

        self.btn_run = QtWidgets.QPushButton("Run")
        l.addWidget(self.btn_run, 3, 5, 1, 1)

        widget.setLayout(l)
