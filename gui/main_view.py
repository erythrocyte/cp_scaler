import logging
from PyQt5 import QtWidgets, QtCore

from gui.ui_main_view import UiMainView


class MainView(QtWidgets.QMainWindow, UiMainView):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup_ui(self)

        self.logger = None
        self.__setup_logger()
        self.__connect()

    def __setup_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('app.log', 'w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        self.logger.addHandler(self.mess)

    def __connect(self):
        self.scaler_view.set_progress.connect(self.__update_progress)
        self.well_intersect_view.set_progress.connect(self.__update_progress)

    @QtCore.pyqtSlot(int, str)
    def __update_progress(self, val: int, txt: str):
        self.progress.setValue(val)        
        self.progress.setFormat(f'{txt} ({val} %)')
