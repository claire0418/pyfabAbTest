
from .CGH import CGH
import numpy as np
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)


class QAberration(CGH):

    correctionReady = pyqtSignal(np.ndarray)
    recalculate = pyqtSignal()

    def __init__(self, *args, **kwargs): 
        super(QAberration, self).__init__(*args, **kwargs)
        self.zernike = self._psi = np.zeros(self.shape)
       
    @pyqtSlot(np.ndarray)
    def correction(self, array):
        r = self.qr
        theta = self.theta
        
        a0 = array[0]
        a1 = array[1]
        a2 = array[2]
        a3 = array[3]
        a4 = array[4]
        a5 = array[5]
        a6 = array[6]
        a7 = array[7]
        a8 = array[8]
        rand = array[9]

        phi = a0 + a1 * r * np.cos(theta) \
                + a2 * r * np.sin(theta) \
                + a3 * (2*r**2 - 1) \
                + a4 * r**2 * np.cos(2*theta) \
                + a5 * r**2 * np.sin(2*theta) \
                + a6 * (3*r**2 - 2) * r * np.cos(theta) \
                + a7 * (3*r**2 - 2) * r * np.sin(theta) \
                + a8 * (6*r**4 - 6*r**2 +1) \
                + rand*np.random.rand(self.shape[0],self.shape[1])

        self.zernike = phi
        self.recalculate.emit()

    def quantize(self, psi):
        return ((128. / np.pi) * (psi) + 127.).astype(np.uint8)
    
    def newcompute(self, phi):
        phi2 = phi + self.quantize(self.zernike)
        self.correctionReady.emit(phi2)
        
        
