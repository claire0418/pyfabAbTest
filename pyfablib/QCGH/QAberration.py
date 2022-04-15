
from .CGH import CGH
import numpy as np
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)


class QAberration(CGH):

    correctionReady = pyqtSignal()

    def __init__(self, *args, **kwargs): # figure this out lol
        super(QAberration, self).__init__(*args, *kwargs)
        self.correction = 0

       
    @pyqtSlot(np.ndarray)
    def correction(array):
        r = self.qr
        theta = self.theta
        
        array[0] = a0
        array[1] = a1
        array[2] = a2
        array[3] = a3
        array[4] = a4
        array[5] = a5
        array[6] = a6
        array[7] = a7
        array[8] = a8

        correction = a0 + a1 * r * np.cos(theta) \
                + a2 * r * np.sin(theta) \
                + a3 * (2*r**2 - 1) \
                + a4 * r**2 * np.cos(2*theta) \
                + a5 * r**2 * np.sin(2*theta) \
                + a6 * (3*r**2 - 2) * r * np.cos(theta) \
                + a7 * (3*r**2 - 2) * r * np.sin(theta) \
                + a8 * (6*r**4 - 6*r**2 +1)

        self.correction = correction
        correctionReady.emit()

    def quantize(psi):
        return ((128. / np.pi) * (psi+self.correction) + 127.).astype(np.uint8)
