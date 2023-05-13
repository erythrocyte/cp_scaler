import logging
import os

from PyQt5 import QtWidgets

from gui.widgets.ui_well_intersect_widget import UiWellIntersectWidget
from src.services import grdecl_reader
from gui.well_inter_calc_prms import WellIntersectCalcParams


class WellIntersectWidget(QtWidgets.QWidget, UiWellIntersectWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setup_ui(self)
        self.__connect()

    def __connect(self):
        self.btn_run.clicked.connect(self.__run_calc)
        self.btn_coord_fn.clicked.connect(self.__set_coord_fn)

    def __run_calc(self):
        try:
            prms = self.__get_calc_params()
            if not self.__check_params(prms):
                return
            grd = grdecl_reader.read_grid(prms.data_fn)
            if grd is None:
                logging.error('Error reading grid')
                return
            self.__update_progress(0)
            # scaled_fig = scaler.scale_coord(
            #     coord, prms.nx, prms.ny, prms.sx, prms.sy, self.__update_progress)
            self.__update_progress(100)
            # if scaled_fig is None:
            #     return

            # d = os.path.dirname(prms.coord_fn)
            # fn_fig = os.path.join(d, f'{prms.new_fn}.dat')
            # coord_writer.write(fn_fig, scaled_fig)
            logging.info(f'Well intersect done')
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
        prms.result_fn = 'result.txt'

        return prms

    def __set_coord_fn(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select Folder', '', options=QtWidgets.QFileDialog.DontUseNativeDialog)

        if fn == '':
            return

        new_fn = f'{os.path.splitext(os.path.basename(fn))[0]}_scaled'

        self.coord_fn.setText(fn)
        self.new_fn.setText(new_fn)

    def __update_progress(self, val):
        self.set_progress.emit(val)
