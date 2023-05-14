from PyQt5 import QtWidgets, QtCore


class UiScalerView:
    set_progress = QtCore.pyqtSignal(int, str)

    def __init__(self):
        self.btn_run = QtWidgets.QPushButton()
        self.nx = None
        self.ny = None
        self.sx = QtWidgets.QDoubleSpinBox()
        self.sy = QtWidgets.QDoubleSpinBox()
        self.coord_fn = QtWidgets.QLineEdit()
        self.new_fn = None
        self.btn_coord_fn = None

    def setup_ui(self, widget: QtWidgets.QWidget):
        self.__createComponents(widget)

    def __createComponents(self, widget: QtWidgets.QWidget):
        l = QtWidgets.QGridLayout()

        # coord
        lbl = QtWidgets.QLabel("Coord file")
        l.addWidget(lbl, 0, 0, 1, 1)
        self.coord_fn = QtWidgets.QLineEdit()
        l.addWidget(self.coord_fn, 0, 1, 1, 4)
        self.btn_coord_fn = QtWidgets.QPushButton("...")
        l.addWidget(self.btn_coord_fn, 0, 5, 1, 1)

        # NX and NY
        lbl_nx = QtWidgets.QLabel("Nx")
        l.addWidget(lbl_nx, 1, 0, 1, 1)
        self.nx = QtWidgets.QSpinBox()
        self.nx.setMinimum(1)
        l.addWidget(self.nx, 1, 1, 1, 2)

        lbl_ny = QtWidgets.QLabel("Ny")
        l.addWidget(lbl_ny, 1, 3, 1, 1)
        self.ny = QtWidgets.QSpinBox()
        self.ny.setMinimum(1)
        l.addWidget(self.ny, 1, 4, 1, 2)

        # NX and NY
        lbl_sx = QtWidgets.QLabel("Sx")
        l.addWidget(lbl_sx, 2, 0, 1, 1)
        self.sx = QtWidgets.QDoubleSpinBox()
        self.sx.setMinimum(1e-8)
        self.sx.setValue(0.1)
        self.sx.setSingleStep(0.1)
        l.addWidget(self.sx, 2, 1, 1, 2)

        lbl_sy = QtWidgets.QLabel("Sy")
        l.addWidget(lbl_sy, 2, 3, 1, 1)
        self.sy = QtWidgets.QDoubleSpinBox()
        self.sy.setMinimum(1e-8)
        self.sy.setValue(0.1)
        self.sy.setSingleStep(0.1)
        l.addWidget(self.sy, 2, 4, 1, 2)

        # new file name
        lbl_new_fn = QtWidgets.QLabel("New file name")
        l.addWidget(lbl_new_fn, 3, 0, 1, 1)
        self.new_fn = QtWidgets.QLineEdit()
        l.addWidget(self.new_fn, 3, 1, 1, 5)

        self.btn_run = QtWidgets.QPushButton("Run")
        l.addWidget(self.btn_run, 4, 5, 1, 1)

        widget.setLayout(l)
