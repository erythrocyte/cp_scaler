import logging
import os

from PyQt5 import QtWidgets

from gui.widgets.ui_scaler_widget import UiScalerWidget
from gui.scaler_calc_prms import CalcParams
from src.services import scaler
from src.services import coord_writer, grdecl_reader


class ScalerWidget(QtWidgets.QWidget, UiScalerWidget):
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
            coord = grdecl_reader.read_coord(prms.coord_fn)
            self.__update_progress(0)            
            scaled_fig = scaler.scale_coord(
                coord, prms.nx, prms.ny, prms.sx, prms.sy, self.__update_progress)
            self.__update_progress(100)
            if scaled_fig is None:
                return

            d = os.path.dirname(prms.coord_fn)
            fn_fig = os.path.join(d, f'{prms.new_fn}.dat')
            coord_writer.write(fn_fig, scaled_fig)
            logging.info(
                f'Coord from file \'{prms.coord_fn}\' scaled and saved to file \'{fn_fig}\' !')
        except Exception as e:
            logging.fatal(f'Fatal error with message: {str(e)}')

    def __check_params(self, prms: CalcParams):
        if prms is None:
            logging.fatal('Unknown error while running calculation')
            return False

        if prms.coord_fn == '':
            logging.error('Coord file is not set')
            return False

        if not os.path.isfile(prms.coord_fn):
            logging.error('Set coord path does not refer to file')
            return False

        if not os.path.exists(prms.coord_fn):
            logging.error('Set coord path does not exist')
            return False

        if prms.new_fn == '':
            logging.error('New file does not set')
            return False

        return True

    def __get_calc_params(self):
        prms = CalcParams()
        prms.coord_fn = self.coord_fn.text()
        prms.nx = self.nx.value()
        prms.ny = self.ny.value()
        prms.sx = self.sx.value()
        prms.sy = self.sy.value()
        prms.new_fn = self.new_fn.text()

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
