#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QStackedLayout)
from PyQt5.QtCore import pyqtSlot

from jansenlib.video import QCamera
from pyfablib.QCGH import CGH
from pyfablib.QSLM import QSLM
from pyfablib.QCGH.QAberration import QAberration
from pyfablib.QCGH.QAbWidget import QAbWidget
from pyfablib.QCGH.QOptimize import QOptimize
from pyfablib.traps import QTrappingPattern
from tasks import (buildTaskMenu, QTaskmanager)
from common.Configuration import Configuration

# Support for HTML Help
from PyQt5 import QtWebEngineWidgets
import help.pyfab_help_rc


import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PyFab(QMainWindow):

    def __init__(self, parent=None, doconfig=True):
        super(PyFab, self).__init__(parent)

        uifile = Path('pyfablib').joinpath('FabWidget.ui')
        uic.loadUi(uifile, self)

        self.configuration = Configuration(self)

        # Camera
        self.camera.close()  # remove placeholder widget from UI
        self.camera = QCamera()
        self.screen.camera = self.camera
        self.cameraLayout.addWidget(self.camera)

        # Spatial light modulator
        self.slm = QSLM(self)
        
        # Computation pipeline
        self.cgh.device = CGH(self, shape=self.slm.shape).start()
        
        #aberration correction
        #self.abwid = QAbWidget(self)
        self.aber = QAberration(self, shape=self.slm.shape).start()
        
        #optimization algorithm
        self.optimization = QOptimize(self, shape=self.slm.shape).start()
        

        # Trapping pattern is an interactive overlay
        # that translates user actions into hologram computations
        self.pattern = QTrappingPattern(parent=self)
        self.screen.addOverlay(self.pattern)

        # Process automation
        self.tasks = QTaskmanager(self)
        self.TaskManagerView.setModel(self.tasks)
        self.TaskManagerView.setSelectionMode(3)

        self.configureUi()
        self.connectSignals()

        self.doconfig = doconfig
        if self.doconfig:
            self.restoreSettings()

    def closeEvent(self, event):
        self.saveSettings()
        self.pattern.clearTraps()
        self.screen.close()
        self.slm.close()
        self.cgh.device.stop()
        self.deleteLater()

    def configureUi(self):
        self.filters.screen = self.screen
        self.histogram.screen = self.screen
        self.dvr.screen = self.screen
        self.dvr.source = self.screen.default
        self.dvr.filename = self.configuration.datadir + 'pyfab.avi'

        self.TaskPropertiesLayout = QStackedLayout(self.TaskPropertiesView)
        index = self.tabWidget.indexOf(self.hardware.parent())
        self.tabWidget.setTabEnabled(index, self.hardware.has_content())
        self.slmView.setRange(xRange=[0, self.slm.width()],
                              yRange=[0, self.slm.height()],
                              padding=0)
        buildTaskMenu(self)
        self.adjustSize()

    def connectSignals(self):
        # Signals associated with arrival of images from camera
        newframe = self.screen.source.sigNewFrame
        # 1. Update histograms from image data
        newframe.connect(self.histogram.updateHistogram)
        # 2. CGH computations are coordinated with camera
        newframe.connect(self.pattern.refresh)

        # Signals associated with the CGH pipeline
        # 1. Screen events trigger requests for trap updates
        self.screen.sigMousePress.connect(self.pattern.mousePress)
        self.screen.sigMouseRelease.connect(self.pattern.mouseRelease)
        self.screen.sigMouseMove.connect(self.pattern.mouseMove)
        self.screen.sigMouseWheel.connect(self.pattern.mouseWheel)
        # 2. Trap widget reflects changes to trapping pattern
        self.pattern.sigCompute.connect(self.cgh.device.compute)
        self.pattern.trapAdded.connect(self.traps.registerTrap)
        
        # 2.5. aberration stuff
        self.aberration.coefs.connect(self.aber.correction)
        self.aber.recalculate.connect(self.pattern.toggleHologram)
        
        # optimization stuff
        self.aberration.optimize.connect(self.pattern.sendTraps)
        self.pattern.optimizeTraps.connect(self.optimization.optimize)
        self.optimization.calculate.connect(self.aber.newcompute)
        self.aberration.unoptimize.connect(self.pattern.toggleHologram)
        
        
        # 3. Project result when calculation is complete
        self.cgh.device.sigHologramReady.connect(self.aber.newcompute)
        self.aber.correctionReady.connect(self.slm.setData)
        self.aber.correctionReady.connect(self.slmView.setData)

        # Signals associated with GUI controls
        # 1. DVR Source
        self.bcamera.clicked.connect(
            lambda: self.setDvrSource(self.screen.default))
        self.bfilters.clicked.connect(
            lambda: self.setDvrSource(self.screen))

        # 2. Tab expose events
        self.tabWidget.currentChanged.connect(self.hardware.expose)
        self.tabWidget.currentChanged.connect(
            lambda n: self.slmView.setData(self.cgh.device.phi))

        # 3. Task pipeline
        self.bpausequeue.clicked.connect(self.pauseTasks)
        self.bclearqueue.clicked.connect(self.stopTasks)

        self.bpausesel.clicked.connect(self.tasks.toggleSelected)
        self.bclearsel.clicked.connect(self.tasks.removeSelected)
        self.bserialize.clicked.connect(
            lambda: self.tasks.serialize(self.experimentPath.text()))
        self.bdeserialize.clicked.connect(
            lambda: self.tasks.registerTask('QExperiment',
                                            info=self.experimentPath.text(),
                                            loop=self.loop.value()))

        self.TaskManagerView.clicked.connect(self.tasks.displayProperties)
        self.TaskManagerView.doubleClicked.connect(self.tasks.toggleCurrent)

    @pyqtSlot()
    def setDvrSource(self, source):
        self.dvr.source = source

    #
    # Slots for menu actions
    #
    def saveImage(self, qimage, select=False):
        if qimage is None:
            return
        filename = self.configuration.filename(suffix='.png')
        if select:
            getname = QFileDialog.getSaveFileName
            filename, _ = getname(self, 'Save Image',
                                  directory=filename,
                                  filter='Image files (*.png)')
        if filename:
            qimage.save(filename)
            self.statusBar().showMessage('Saved ' + filename)

    @pyqtSlot()
    def savePhoto(self, select=False):
        qimage = self.screen.imageItem.qimage
        self.saveImage(qimage, select=select)

    @pyqtSlot()
    def savePhotoAs(self):
        self.savePhoto(select=True)

    @pyqtSlot()
    def saveHologram(self, select=False):
        self.saveImage(self.slm.qimage, select=select)

    @pyqtSlot()
    def saveHologramAs(self):
        self.saveHologram(select=True)

    @pyqtSlot()
    def saveSettings(self):
        if self.doconfig:
            self.configuration.save(self.camera)
            self.configuration.save(self.cgh)

    @pyqtSlot()
    def restoreSettings(self):
        if self.doconfig:
            self.configuration.restore(self.camera)
            self.configuration.restore(self.cgh)

    @pyqtSlot()
    def pauseTasks(self):
        self.tasks.pauseTasks()
        msg = 'Tasks paused' if self.tasks.paused else 'Tasks running'
        self.statusBar().showMessage(msg)

    @pyqtSlot()
    def stopTasks(self):
        self.tasks.clearTasks()
        self.statusBar().showMessage('Task queue cleared')


def main():
    import sys
    import argparse
    from PyQt5.QtWidgets import QApplication

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--noconfig',
                        dest='doconfig', action='store_false',
                        help='Do not use saved configuration data')

    args, unparsed = parser.parse_known_args()
    qt_args = sys.argv[:1] + unparsed

    app = QApplication(qt_args)
    win = PyFab(doconfig=args.doconfig)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
