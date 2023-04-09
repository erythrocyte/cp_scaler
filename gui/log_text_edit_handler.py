"""
module docstring
"""

import logging
from PyQt5 import QtWidgets


class LogTextEditHandler(logging.Handler):
    """
    Doc string
    """

    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.setLevel(logging.INFO)
        self.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'))

    def emit(self, record):
        frmt_msg = self.format(record)
        msg = self.__beatify_message(frmt_msg, record.levelname)
        self.widget.appendHtml(msg)

    @staticmethod
    def __beatify_message(msg: str, log_level: str):
        """
        beautify the message according to log level
        """

        if log_level == 'WARNING':
            return f'<font color=\"Orange\">{msg}</font>'

        if log_level == 'ERROR' or log_level == 'CRITICAL':
            return f'<font color=\"Red\">{msg}</font>'

        return msg