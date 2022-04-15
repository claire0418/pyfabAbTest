
from .CGH import CGH
import numpy as np


class QAberration(CGH)

    correctionReady = pyqtSignal()

    def __init__(self, *args, **kwargs) # figure this out lol
        super(QAberration, self).__init__(*args, *kwargs)
        self.correction = 0

    def correction(a0,a1,a2,a3,a4,a5,a6,a7,a8):
        r = self.qr
        theta = self.theta

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
