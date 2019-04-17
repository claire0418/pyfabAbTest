# -*- coding: utf-8 -*-

from PyQt5.QtCore import (QObject, QThread, QEvent,
                          pyqtSignal, pyqtSlot, pyqtProperty)
from PyQt5.QtWidgets import (QFrame, QStyle, QFileDialog)
from .QDVRWidget import Ui_QDVRWidget
from jansenlib.video.QVideoPlayer import QVideoPlayer
import cv2
import numpy as np
import os
import platform

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def clickable(widget):
    """Adds a clicked signal to a widget such as QLineEdit that
    ordinarily does not provide notifications of clicks."""

    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


class QWriter(QObject):

    sigFrameNumber = pyqtSignal(int)
    sigFinished = pyqtSignal()

    def __init__(self, dvr, nframes=10000):
        super(QWriter, self).__init__()
        self.shape = dvr.source.shape
        color = (len(self.shape) == 3)
        h, w = self.shape[0:2]
        fps = 24
        msg = 'Recording: {}x{}, color: {}, fps: {}'
        logger.info(msg.format(w, h, color, fps))
        self.writer = cv2.VideoWriter(dvr.filename,
                                      dvr._fourcc,
                                      fps, (w, h), color)
        self.framenumber = 0
        self.target = nframes
        self.sigFrameNumber.emit(self.framenumber)

    @pyqtSlot(np.ndarray)
    def write(self, frame):
        if ((frame.shape != self.shape) or
                (self.framenumber >= self.target)):
            self.sigFinished.emit()
            return
        self.writer.write(frame)
        self.framenumber += 1
        self.sigFrameNumber.emit(self.framenumber)

    @pyqtSlot()
    def close(self):
        self.writer.release()


class QDVR(QFrame):

    recording = pyqtSignal(bool)

    def __init__(self,
                 parent=None,
                 source=None,
                 screen=None,
                 filename='~/data/fabdvr.avi',
                 codec=None):
        super(QDVR, self).__init__(parent)

        self._writer = None
        self._player = None
        if codec is None:
            if platform.system() == 'Linux':
                codec = 'HFYU'
            else:
                codec = 'X264'
        if cv2.__version__.startswith('2.'):
            self._fourcc = cv2.cv.CV_FOURCC(*codec)
        else:
            self._fourcc = cv2.VideoWriter_fourcc(*codec)
        self._framenumber = 0
        self._nframes = 0

        self.ui = Ui_QDVRWidget()
        self.ui.setupUi(self)
        self.connectSignals()

        self.source = source
        self.screen = screen
        self.filename = filename

    def connectSignals(self):
        clickable(self.ui.playEdit).connect(self.getPlayFilename)
        clickable(self.ui.saveEdit).connect(self.getSaveFilename)
        self.ui.recordButton.clicked.connect(self.record)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.rewindButton.clicked.connect(self.rewind)
        self.ui.pauseButton.clicked.connect(self.pause)
        self.ui.playButton.clicked.connect(self.play)

    def is_recording(self):
        return (self._writer is not None)

    def is_playing(self):
        return (self._player is not None)

    # =====
    # Slots
    #

    @pyqtSlot()
    def getPlayFilename(self):
        if self.is_recording():
            return
        filename, _filter = QFileDialog.getOpenFileName(
            self, 'Video File Name', self.filename, 'Video files (*.avi)')
        if filename:
            self.playname = str(filename)

    @pyqtSlot()
    def getSaveFilename(self):
        if self.is_recording():
            return
        filename, _filter = QFileDialog.getSaveFileName(
            self, 'Video File Name', self.filename, 'Video files (*.avi)')
        if filename:
            self.filename = str(filename)

    # Record functionality

    @pyqtSlot()
    def record(self, nframes=10000):
        if (self.is_recording() or self.is_playing() or (nframes <= 0)):
            return
        logger.debug('Starting Recording')
        self._writer = QWriter(self)
        self._writer.sigFrameNumber.connect(self.setFrameNumber)
        self._writer.sigFinished.connect(self.stop)
        self._thread = QThread()
        self._thread.finished.connect(self._writer.close)
        self.source.sigNewFrame.connect(self._writer.write)
        self._writer.moveToThread(self._thread)
        self._thread.start()
        self.recording.emit(True)

    @pyqtSlot()
    def stop(self):
        if self.is_recording():
            logger.debug('Stopping Recording')
            self._thread.quit()
            self._thread.wait()
            self._thread = None
            self._writer = None
        if self.is_playing():
            logger.debug('Stopping Playing')
            self._player.stop()
            self._player = None
            self.screen.source = None  # use default source
        self.framenumber = 0
        self._nframes = 0
        self.recording.emit(False)

    @pyqtSlot(int)
    def setFrameNumber(self, framenumber):
        self.framenumber = framenumber

    # Playback functionality

    @pyqtSlot()
    def play(self):
        if self.is_recording():
            return
        if self.is_playing():
            self._player.pause(False)
            return
        logger.debug('Starting Playback')
        self.framenumber = 0
        self._player = QVideoPlayer(self, self.playname)
        self._player.sigNewFrame.connect(self.stepFrameNumber)
        self._player.start()
        self.screen.source = self._player

    @pyqtSlot()
    def rewind(self):
        if self.is_playing():
            self._player.rewind()
            self.framenumber = 0

    @pyqtSlot()
    def pause(self):
        if self.is_playing():
            state = self._player.isPaused()
            self._player.pause(not state)

    @pyqtSlot()
    def stepFrameNumber(self):
        self.framenumber += 1

    # ==========
    # Properties
    #

    @pyqtProperty(QObject)
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source
        self.ui.recordButton.setEnabled(source is not None)

    @pyqtProperty(QObject)
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen = screen
        self.ui.playButton.setEnabled(screen is not None)

    @pyqtProperty(str)
    def filename(self):
        return str(self.ui.saveEdit.text())

    @filename.setter
    def filename(self, filename):
        if not (self.is_recording() or self.is_playing()):
            self.ui.saveEdit.setText(os.path.expanduser(filename))
            self.playname = self.filename

    @pyqtProperty(str)
    def playname(self):
        return str(self.ui.playEdit.text())

    @playname.setter
    def playname(self, filename):
        if not (self.is_playing()):
            self.ui.playEdit.setText(os.path.expanduser(filename))

    @pyqtProperty(int)
    def framenumber(self):
        return self._framenumber

    @framenumber.setter
    def framenumber(self, number):
        self._framenumber = number
        self.ui.frameNumber.display(self._framenumber)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wid = QDVR()
    wid.show()
    sys.exit(app.exec_())
