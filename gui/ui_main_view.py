import functools
from PyQt5 import QtWidgets, QtCore, QtGui

from gui import prog, log_text_edit_handler


class UiMainView:
    def __init__(self):
        self.__window_title = f'{prog.PRODUCT_NAME} v.{prog.PRODUCT_VERSION}'
        self.mess = None
        self.btn_run = QtWidgets.QPushButton()
        self.nx = None
        self.ny = None
        self.sx = QtWidgets.QDoubleSpinBox()
        self.sy = QtWidgets.QDoubleSpinBox()
        self.coord_fn = QtWidgets.QLineEdit()
        self.new_fn = None
        self.btn_coord_fn = None

    def setup_ui(self, widget: QtWidgets.QMainWindow):
        widget.setMinimumSize(QtCore.QSize(600, 400))
        widget.setFixedSize(QtCore.QSize(600, 400))
        widget.setWindowTitle(self.__window_title)

        self.__createMenuBar(widget)
        self.__createComponents(widget)

    def __createComponents(self, widget: QtWidgets.QMainWindow):
        cw = QtWidgets.QTabWidget(widget)
        widget.setCentralWidget(cw)
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

        self.mess = log_text_edit_handler.LogTextEditHandler(widget)
        l.addWidget(self.mess.widget, 4, 0, 3, 6)

        self.progress = QtWidgets.QProgressBar()
        l.addWidget(self.progress, 7, 0, 1, 4)
        self.btn_run = QtWidgets.QPushButton("Run")
        l.addWidget(self.btn_run, 7, 5, 1, 1)

        cw.setLayout(l)

    def __createMenuBar(self, widget):
        self.menu_bar = QtWidgets.QMenuBar(widget)

        # -- File
        self.__menuBarFile(widget)

        # --- Help
        self.__menuBarHelp(widget)
        widget.setMenuBar(self.menu_bar)

    def __menuBarFile(self, widget):
        self.__file_menu = QtWidgets.QMenu('&File', widget)
        self.menu_bar.addMenu(self.__file_menu)

        self.__close_action = QtWidgets.QAction(QtGui.QIcon(":/power_off"),
                                                '&Close', widget)
        self.__close_action.triggered.connect(widget.close)
        self.__file_menu.addAction(self.__close_action)

    def __menuBarHelp(self, widget):
        self.__help_menu = QtWidgets.QMenu('&Help', widget)
        self.menu_bar.addMenu(self.__help_menu)

        # prod
        self.__about_prod = QtWidgets.QAction('About CPScaler', widget)
        self.__about_prod.triggered.connect(functools.partial(
            QtWidgets.QMessageBox.about,
            widget,
            'About CPScaler',
            """
            < b > Corner point coord scaler < /b >
            < br >< br > Version {0} <br><br>
            <a href="http://{1}/releases/latest">{1}</a>
            """.format(prog.PRODUCT_VERSION, "www.github.com/erythrocyte/cp_scaler/")))
        self.__help_menu.addAction(self.__about_prod)

        # instruction
        self.__prod_user_manual = QtWidgets.QAction('User manual', widget)
        self.__prod_user_manual.triggered.connect(functools.partial(
            QtWidgets.QMessageBox.information,
            widget,
            'User manual',
            """
            <b> Concise user manual </b>
            <br></br>
            <ol> 
                <li> Set the path to a coord file (file with COORD keyword and data). To select file click to "..." button, or 
                copy path manually </li>
                <li>Set the nx and ny size of the grid</li>
                <li>Set the coefficients for scale Ox (i) and Oy (j) axes</li>
                <li> Set the name of a new file where scaled coord data will be written (at the same directory where the original file is)</li>
            </ol>
            """))
        self.__help_menu.addAction(self.__prod_user_manual)

        # qt
        self.__aboutqt = QtWidgets.QAction('About Qt', widget)
        self.__aboutqt.triggered.connect(QtWidgets.QApplication.aboutQt)
        self.__help_menu.addAction(self.__aboutqt)
