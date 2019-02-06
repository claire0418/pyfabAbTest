# -*- coding: utf-8 -*-

"""QSpinnakerThread.py: Spinnaker video camera running in a QThread"""

from pyqtgraph.Qt import QtCore
from QSpinnakerCamera import QSpinnakerCamera
import numpy as np
import cv2

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class QSpinnakerThread(QtCore.QThread):

    """Spinnaker camera

    Continuously captures frames from a video camera,
    emitting sigNewFrame when each frame becomes available.

    NOTE: Subclassing QThread is appealing for this application
    because reading frames is blocking and I/O-bound, but not
    computationally expensive.  QThread moves the read operation
    into a separate thread via the overridden run() method
    while other methods and properties remain available in
    the calling thread.  This simplifies getting and setting
    the camera's properties.

    NOTE: This implementation only moves the camera's read()
    method into a separate thread, not the entire camera.
    FIXME: Confirm that this is acceptable practice.
    """

    sigNewFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self,
                 parent=None,
                 mirrored=False,
                 flipped=True,
                 transposed=False,
                 gray=False):
        super(QSpinnakerThread, self).__init__(parent)

        self.camera = QSpinnakerCamera()
        self.read = self.camera.read
        # camera properties
        self.mirrored = bool(mirrored)
        self.flipped = bool(flipped)
        # self.transposed = bool(transposed)
        self.gray = bool(gray)
        ready, self.frame = self.read()

    def run(self):
        self.running = True
        while self.running:
            ready, self.frame = self.read()
            if ready:
                self.sigNewFrame.emit(self.frame)
        del self.camera

    def stop(self):
        self.running = False

    @property
    def gray(self):
        return self.camera.gray

    @gray.setter
    def gray(self, state):
        self.camera.gray = bool(state)

    @property
    def mirrored(self):
        return self.camera.mirrored

    @mirrored.setter
    def mirrored(self, state):
        self.camera.mirrored = bool(state)

    @property
    def flipped(self):
        return self._flipped

    @flipped.setter
    def flipped(self, state):
        self._flipped = bool(state)

    @property
    def transposed(self):
        return self.mirrored and self.flipped

    @transposed.setter
    def transposed(self, state):
        self.mirrored = bool(state)
        self.transposed = bool(state)

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, image):
        (self._height, self._width) = image.shape[:2]
        if self.flipped:
            image = cv2.flip(image, 0)
        self._frame = image

    def width(self):
        return self.camera.width

    def setWidth(self, width):
        self.camera.width = width
        logger.info('Setting camera width: {}'.format(width))

    def height(self):
        return self.camera.height

    def setHeight(self, height):
        self.camera.height = height
        logger.info('Setting camera height: {}'.format(height))

    @property
    def size(self):
        return QtCore.QSize(self.width(), self.height())

    @size.setter
    def size(self, size):
        if size is None:
            return
        if isinstance(size, QtCore.QSize):
            self.setWidth(size.width())
            self.setHeight(size.height())
        else:
            self.setWidth(size[0])
            self.setHeight(size[1])

    @property
    def roi(self):
        x0 = float(self.camera.x0)
        y0 = float(self.camera.y0)
        return QtCore.QRectF(x0, y0, self.width(), self.height())
