import logging
import os

from PyQt5 import QtWidgets

from gui.views.ui_well_intersect_view import UiWellIntersectView
from src.services import grdecl_reader
from gui.models.well_inter_calc_prms import WellIntersectCalcParams
from gui.presenters import well_intersect_presenter


class WellIntersectView(QtWidgets.QWidget, UiWellIntersectView):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setup_ui(self)
        self.__connect()

        self.data_fn.setText(
            '/home/erythrocyte/Documents/move/GRID_MANIPULATION/WELL_INTERSECT/GRID.grdecl')
        self.well_track_fn.setText(
            '/home/erythrocyte/Documents/move/GRID_MANIPULATION/WELL_INTERSECT/well_track.txt')
        self.result_fn.setText(
            '/home/erythrocyte/Documents/move/GRID_MANIPULATION/WELL_INTERSECT/1.txt')

    def __connect(self):
        self.btn_run.clicked.connect(self.__run_calc)
        self.btn_data_fn.clicked.connect(self.__set_data_fn)
        self.btn_wt_fn.clicked.connect(self.__set_wt_fn)
        self.btn_result_fn.clicked.connect(self.__set_result_fn)

    def __run_calc(self):
        def pp(val, txt):
            self.set_progress.emit(val, txt)

        try:
            prms = self.__get_calc_params()
            if not self.__check_params(prms):
                return

            well_intersect_presenter.calc(prms, pp)
        except Exception as e:
            logging.fatal(f'Fatal error with message: {str(e)}')

    def __check_params(self, prms: WellIntersectCalcParams):
        if prms is None:
            logging.fatal('Unknown error while running calculation')
            return False

        if prms.data_fn == '':
            logging.error('Data file is not set')
            return False

        if not os.path.isfile(prms.data_fn):
            logging.error('Set data path does not refer to file')
            return False

        if not os.path.exists(prms.data_fn):
            logging.error('Set data path does not exist')
            return False

        if prms.well_track_fn == '':
            logging.error('Well track file is not set')
            return False

        if not os.path.isfile(prms.well_track_fn):
            logging.error('Set well track path does not refer to file')
            return False

        if not os.path.exists(prms.well_track_fn):
            logging.error('Set well track path does not exist')
            return False

        if prms.result_fn == '':
            logging.error('Result file does not set')
            return False

        return True

    def __get_calc_params(self):
        prms = WellIntersectCalcParams()
        prms.data_fn = self.data_fn.text()
        prms.well_track_fn = self.well_track_fn.text()
        prms.result_fn = self.result_fn.text()

        return prms

    def __set_data_fn(self):
        fn = self.__get_fn()
        if fn == '':
            return

        self.data_fn.setText(fn)

    def __set_wt_fn(self):
        fn = self.__get_fn()
        if fn == '':
            return

        self.well_track_fn.setText(fn)

    def __set_result_fn(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Select File to Save')
        if fn == '':
            return

        self.result_fn.setText(fn)

    def __get_fn(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select File', '', options=QtWidgets.QFileDialog.DontUseNativeDialog)

        return fn
