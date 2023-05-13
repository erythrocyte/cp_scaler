import functools
from PyQt5 import QtWidgets, QtCore, QtGui

from gui import prog, log_text_edit_handler
from gui.widgets import scaler_widget


class UiMainView:
    def __init__(self):
        self.__window_title = f'{prog.PRODUCT_NAME} v.{prog.PRODUCT_VERSION}'
        self.mess = None
        self.scaler_view = None
        self.splitter = None

    def setup_ui(self, widget: QtWidgets.QMainWindow):
        widget.setMinimumSize(QtCore.QSize(600, 400))
        widget.setFixedSize(QtCore.QSize(600, 400))
        widget.setWindowTitle(self.__window_title)

        self.__createMenuBar(widget)
        self.__createComponents(widget)

    def __createComponents(self, widget: QtWidgets.QMainWindow):
        cw = QtWidgets.QWidget(widget)

        self.splitter = QtWidgets.QSplitter(cw)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setSizes([200, 100])
        widget.setCentralWidget(cw)
        l = QtWidgets.QGridLayout()

        tab = QtWidgets.QTabWidget(cw)
        self.mess = log_text_edit_handler.LogTextEditHandler(widget)

        self.splitter.addWidget(tab)
        self.splitter.addWidget(self.mess.widget)

        l.addWidget(self.splitter, 0, 0, 1, 6)
        self.progress = QtWidgets.QProgressBar()
        l.addWidget(self.progress, 1, 0, 1, 4)

        self.scaler_view = scaler_widget.ScalerWidget()
        tab.addTab(self.scaler_view, "Scaler")

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
