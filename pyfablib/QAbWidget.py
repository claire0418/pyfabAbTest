
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
import numpy as np


class QAbWidget(QWidget):

    coefs = pyqtSignal(float, float, float, float, float, float, float, float, float) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = self._loadUi(Path('pyfablib').joinpath('AbWidget.ui'))
        self._connectSignals()

    def _loadUi(self, uifile):
        form, _ = uic.loadUiType(uifile)
        ui = form()
        ui.setupUi(self)
        return ui

    def _connectSignals(self):
            self.ui.a0slid.valueChanged.connect(self.updateCoefs)
            self.ui.a1slid.valueChanged.connect(self.updateCoefs)
            self.ui.a2slid.valueChanged.connect(self.updateCoefs)
            self.ui.a3slid.valueChanged.connect(self.updateCoefs)
            self.ui.a4slid.valueChanged.connect(self.updateCoefs)
            self.ui.a5slid.valueChanged.connect(self.updateCoefs)
            self.ui.a6slid.valueChanged.connect(self.updateCoefs)
            self.ui.a7slid.valueChanged.connect(self.updateCoefs)
            self.ui.a8slid.valueChanged.connect(self.updateCoefs)

    def updateCoefs(self):
        
        # define coefs from the slider values
        a0 = float(self.ui.a0slid.value()/100.)
        a1 = float(self.ui.a1slid.value()/100.)
        a2 = float(self.ui.a2slid.value()/100.)
        a3 = float(self.ui.a3slid.value()/100.)
        a4 = float(self.ui.a4slid.value()/100.)
        a5 = float(self.ui.a5slid.value()/100.)
        a6 = float(self.ui.a6slid.value()/100.)
        a7 = float(self.ui.a7slid.value()/100.)
        a8 = float(self.ui.a8slid.value()/100.)
        
        # set value for spinboxes on widget
        self.ui.a0.setValue(a0)
        self.ui.a1.setValue(a1)
        self.ui.a2.setValue(a2)
        self.ui.a3.setValue(a3)
        self.ui.a4.setValue(a4)
        self.ui.a5.setValue(a5)
        self.ui.a6.setValue(a6)
        self.ui.a7.setValue(a7)
        self.ui.a8.setValue(a8)

        # ugh
        self.coefs.emit(a0,a1,a2,a3,a4,a5,a6,a7,a8)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = QAbWidget()
    widget.show()
    sys.exit(app.exec_())
