
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import (QWidget, QFrame)
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
from .AbWidget import Ui_Form
import numpy as np


class QAbWidget(QFrame):

    coefs = pyqtSignal(np.ndarray) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._connectSignals()

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
            self.ui.randomslider.valueChanged.connect(self.updateCoefs)
            self.ui.Reset.clicked.connect(self.reset)

    def updateCoefs(self):
        
        # define coefficients from the slider values
        a0 = np.pi*self.ui.a0slid.value()/100.
        a1 = np.pi*self.ui.a1slid.value()/100.
        a2 = np.pi*self.ui.a2slid.value()/100.
        a3 = np.pi*self.ui.a3slid.value()/100.
        a4 = np.pi*self.ui.a4slid.value()/100.
        a5 = np.pi*self.ui.a5slid.value()/100.
        a6 = np.pi*self.ui.a6slid.value()/100.
        a7 = np.pi*self.ui.a7slid.value()/100.
        a8 = np.pi*self.ui.a8slid.value()/100.
        rand = np.pi*self.ui.randomslider.value()/100.
        
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

        # send coefficients
        self.coefs.emit(np.array([a0,a1,a2,a3,a4,a5,a6,a7,a8,rand]))
        
    def reset(self):
        self.ui.a0slid.setValue(0)
        self.ui.a1slid.setValue(0)
        self.ui.a2slid.setValue(0)
        self.ui.a3slid.setValue(0)
        self.ui.a4slid.setValue(0)
        self.ui.a5slid.setValue(0)
        self.ui.a6slid.setValue(0)
        self.ui.a7slid.setValue(0)
        self.ui.a8slid.setValue(0)
        self.updateCoefs()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = QAbWidget()
    widget.show()
    sys.exit(app.exec_())
