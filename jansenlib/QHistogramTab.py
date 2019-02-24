# -*- coding: utf-8 -*-

"""Visualization of image histograms."""

import PyQt5
from PyQt5.QtWidgets import (QFrame, QLabel)
import pyqtgraph as pg
from common.tabLayout import tabLayout
import numpy as np
import cv2


class QHistogramTab(QFrame):

    def __init__(self, video, parent=None):
        super(QHistogramTab, self).__init__(parent)

        self.title = 'Histogram'
        self.index = -1
        self.video = video

        self.setFrameShape(QFrame.Box)
        layout = tabLayout(self)

        title = QLabel('Histogram')
        layout.addWidget(title)
        histo = self.plotWidget('Intensity', 'N(Intensity)', height=250)
        histo.setXRange(0, 255)
        self.rplot = histo.plot()
        self.rplot.setPen('r', width=2)
        self.gplot = histo.plot()
        self.gplot.setPen('g', width=2)
        self.bplot = histo.plot()
        self.bplot.setPen('b', width=2)
        layout.addWidget(histo)

        title = QLabel('Horizontal Profile')
        layout.addWidget(title)
        xmean = self.plotWidget('x [pixel]', 'I(x)')
        self.xplot = xmean.plot()
        self.xplot.setPen('r', width=2)
        layout.addWidget(xmean)

        title = QLabel('Vertical Profile')
        layout.addWidget(title)
        ymean = self.plotWidget('y [pixel]', 'I(y)')
        self.yplot = ymean.plot()
        self.yplot.setPen('r', width=2)
        layout.addWidget(ymean)

    def plotWidget(self, xlabel, ylabel, height=150):
        wid = pg.PlotWidget(background='w')
        wid.getAxis('bottom').setPen(0.1)
        wid.getAxis('left').setPen(0.1)
        wid.showGrid(x=True, y=True)
        wid.setMouseEnabled(x=False, y=False)
        wid.setMaximumHeight(height)
        wid.setLabel('bottom', xlabel)
        wid.setLabel('left', ylabel)
        return wid

    def expose(self, index):
        if index == self.index:
            self.video.registerFilter(self.histogramFilter)
        else:
            self.video.unregisterFilter(self.histogramFilter)

    def histogramFilter(self, frame):
        if frame.ndim == 2:
            y = np.bincount(frame.flat, minlength=256)
            self.rplot.setData(y=y)
            self.gplot.setData(y=[0, 0])
            self.bplot.setData(y=[0, 0])
            self.xplot.setData(y=np.mean(frame, 0))
            self.yplot.setData(y=np.mean(frame, 1))
        else:
            b, g, r = cv2.split(frame)
            y = np.bincount(r.flat, minlength=256)
            self.rplot.setData(y=y)
            y = np.bincount(g.flat, minlength=256)
            self.gplot.setData(y=y)
            y = np.bincount(b.flat, minlength=256)
            self.bplot.setData(y=y)
            self.xplot.setData(y=np.mean(r, 0))
            self.yplot.setData(y=np.mean(r, 1))
        return frame
