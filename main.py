# -*- coding: utf-8 -*-
"""
@author: Jayalath A M Madawa Abeywardhana

Useful references>>
Qt tutorials : http://zetcode.com/gui/pyqt5/layout/
for QtSql: >> apt-get install python-pyqt5.qtsql
"""

import sys
from PyQt5.QtWidgets import QApplication

import gui


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainGui = gui.GUI()

    sys.exit(app.exec_())
