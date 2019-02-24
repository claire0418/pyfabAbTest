#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.QSettingsWidget import QSettingsWidget
from QOpenCVWidget import Ui_QOpenCVWidget
from QOpenCVThread import QOpenCVThread

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class QOpenCV(QSettingsWidget):

    '''Camera widget based on OpenCV'''

    def __init__(self, parent=None, device=None, **kwargs):
        if device is None:
            device = QOpenCVThread(**kwargs)
        self.thread = device
        self.sigNewFrame = self.thread.sigNewFrame
        ui = Ui_QOpenCVWidget()
        super(QOpenCV, self).__init__(parent,
                                      device=device,
                                      ui=ui)
        self.thread.start()

    def configureUi(self):
        logger.debug('configuring UI')
        self.ui.width.setMaximum(self.thread.camera.width)
        self.ui.height.setMaximum(self.thread.camera.height)

    def close(self):
        logger.debug('Closing camera interface')
        self.device = None
        self.thread.stop()
        self.thread.quit()
        self.thread.wait()

    def closeEvent(self):
        self.close


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    device = QOpenCVThread()
    wid = QOpenCV(device=device)
    wid.show()
    sys.edit(app.exec_())


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    device = QOpenCVThread()
    wid = QOpenCV(device=device)
    wid.show()
    print(wid.shape)
    sys.exit(app.exec_())
