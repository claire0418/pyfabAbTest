# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QSpinnakerWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QSpinnakerWidget(object):
    def setupUi(self, QSpinnakerWidget):
        QSpinnakerWidget.setObjectName("QSpinnakerWidget")
        QSpinnakerWidget.resize(248, 244)
        QSpinnakerWidget.setMinimumSize(QtCore.QSize(248, 244))
        self.verticalLayout = QtWidgets.QVBoxLayout(QSpinnakerWidget)
        self.verticalLayout.setContentsMargins(3, 1, 3, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameFlip = QtWidgets.QFrame(QSpinnakerWidget)
        self.frameFlip.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameFlip.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameFlip.setObjectName("frameFlip")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frameFlip)
        self.horizontalLayout_2.setContentsMargins(3, 1, 3, 1)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mirrored = QtWidgets.QCheckBox(self.frameFlip)
        self.mirrored.setObjectName("mirrored")
        self.horizontalLayout_2.addWidget(self.mirrored)
        spacerItem = QtWidgets.QSpacerItem(103, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.flipped = QtWidgets.QCheckBox(self.frameFlip)
        self.flipped.setObjectName("flipped")
        self.horizontalLayout_2.addWidget(self.flipped)
        self.verticalLayout.addWidget(self.frameFlip)
        self.frameExposure = QtWidgets.QFrame(QSpinnakerWidget)
        self.frameExposure.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameExposure.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameExposure.setObjectName("frameExposure")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameExposure)
        self.gridLayout_2.setContentsMargins(3, 1, 3, 1)
        self.gridLayout_2.setHorizontalSpacing(2)
        self.gridLayout_2.setVerticalSpacing(1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gainLabel = QtWidgets.QLabel(self.frameExposure)
        self.gainLabel.setObjectName("gainLabel")
        self.gridLayout_2.addWidget(self.gainLabel, 1, 0, 1, 1)
        self.autogain = QtWidgets.QPushButton(self.frameExposure)
        self.autogain.setObjectName("autogain")
        self.gridLayout_2.addWidget(self.autogain, 1, 2, 1, 1)
        self.gain = QtWidgets.QDoubleSpinBox(self.frameExposure)
        self.gain.setDecimals(1)
        self.gain.setMaximum(24.0)
        self.gain.setSingleStep(0.1)
        self.gain.setObjectName("gain")
        self.gridLayout_2.addWidget(self.gain, 1, 1, 1, 1)
        self.labelblacklevel = QtWidgets.QLabel(self.frameExposure)
        self.labelblacklevel.setObjectName("labelblacklevel")
        self.gridLayout_2.addWidget(self.labelblacklevel, 2, 0, 1, 1)
        self.blacklevel = QtWidgets.QDoubleSpinBox(self.frameExposure)
        self.blacklevel.setDecimals(3)
        self.blacklevel.setSingleStep(0.1)
        self.blacklevel.setProperty("value", 1.5)
        self.blacklevel.setObjectName("blacklevel")
        self.gridLayout_2.addWidget(self.blacklevel, 2, 1, 1, 1)
        self.exposure = QtWidgets.QDoubleSpinBox(self.frameExposure)
        self.exposure.setDecimals(0)
        self.exposure.setMinimum(10.0)
        self.exposure.setMaximum(50000.0)
        self.exposure.setSingleStep(10.0)
        self.exposure.setObjectName("exposure")
        self.gridLayout_2.addWidget(self.exposure, 0, 1, 1, 1)
        self.exposureLabel = QtWidgets.QLabel(self.frameExposure)
        self.exposureLabel.setObjectName("exposureLabel")
        self.gridLayout_2.addWidget(self.exposureLabel, 0, 0, 1, 1)
        self.autoexposure = QtWidgets.QPushButton(self.frameExposure)
        self.autoexposure.setObjectName("autoexposure")
        self.gridLayout_2.addWidget(self.autoexposure, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.frameExposure)
        self.frameGamma = QtWidgets.QFrame(QSpinnakerWidget)
        self.frameGamma.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameGamma.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameGamma.setObjectName("frameGamma")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frameGamma)
        self.gridLayout_3.setContentsMargins(3, 1, 3, 1)
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelgamma = QtWidgets.QLabel(self.frameGamma)
        self.labelgamma.setObjectName("labelgamma")
        self.gridLayout_3.addWidget(self.labelgamma, 0, 0, 1, 1)
        self.labelsharpness = QtWidgets.QLabel(self.frameGamma)
        self.labelsharpness.setObjectName("labelsharpness")
        self.gridLayout_3.addWidget(self.labelsharpness, 0, 1, 1, 1)
        self.gamma = QtWidgets.QDoubleSpinBox(self.frameGamma)
        self.gamma.setMinimum(0.5)
        self.gamma.setMaximum(4.0)
        self.gamma.setSingleStep(0.1)
        self.gamma.setProperty("value", 1.0)
        self.gamma.setObjectName("gamma")
        self.gridLayout_3.addWidget(self.gamma, 1, 0, 1, 1)
        self.sharpness = QtWidgets.QSpinBox(self.frameGamma)
        self.sharpness.setMinimum(1)
        self.sharpness.setMaximum(1024)
        self.sharpness.setProperty("value", 512)
        self.sharpness.setObjectName("sharpness")
        self.gridLayout_3.addWidget(self.sharpness, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frameGamma)
        self.frameMode = QtWidgets.QFrame(QSpinnakerWidget)
        self.frameMode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameMode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMode.setObjectName("frameMode")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frameMode)
        self.gridLayout_4.setContentsMargins(3, 1, 3, 1)
        self.gridLayout_4.setHorizontalSpacing(2)
        self.gridLayout_4.setVerticalSpacing(1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelVideoMode = QtWidgets.QLabel(self.frameMode)
        self.labelVideoMode.setObjectName("labelVideoMode")
        self.gridLayout_4.addWidget(self.labelVideoMode, 0, 0, 1, 1)
        self.labelFrameRate = QtWidgets.QLabel(self.frameMode)
        self.labelFrameRate.setObjectName("labelFrameRate")
        self.gridLayout_4.addWidget(self.labelFrameRate, 0, 1, 1, 1)
        self.videomode = QtWidgets.QComboBox(self.frameMode)
        self.videomode.setObjectName("videomode")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.videomode.addItem("")
        self.gridLayout_4.addWidget(self.videomode, 1, 0, 1, 1)
        self.framerate = QtWidgets.QDoubleSpinBox(self.frameMode)
        self.framerate.setDecimals(1)
        self.framerate.setMinimum(2.0)
        self.framerate.setMaximum(40.0)
        self.framerate.setProperty("value", 40.0)
        self.framerate.setObjectName("framerate")
        self.gridLayout_4.addWidget(self.framerate, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frameMode)
        self.frameGeometry = QtWidgets.QFrame(QSpinnakerWidget)
        self.frameGeometry.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameGeometry.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameGeometry.setObjectName("frameGeometry")
        self.gridLayout = QtWidgets.QGridLayout(self.frameGeometry)
        self.gridLayout.setContentsMargins(3, 1, 3, 1)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labely0 = QtWidgets.QLabel(self.frameGeometry)
        self.labely0.setObjectName("labely0")
        self.gridLayout.addWidget(self.labely0, 1, 1, 1, 1)
        self.x0 = QtWidgets.QSpinBox(self.frameGeometry)
        self.x0.setObjectName("x0")
        self.gridLayout.addWidget(self.x0, 3, 0, 1, 1)
        self.height = QtWidgets.QSpinBox(self.frameGeometry)
        self.height.setMinimum(16)
        self.height.setMaximum(1080)
        self.height.setSingleStep(16)
        self.height.setProperty("value", 1080)
        self.height.setObjectName("height")
        self.gridLayout.addWidget(self.height, 3, 4, 1, 1)
        self.labelheight = QtWidgets.QLabel(self.frameGeometry)
        self.labelheight.setObjectName("labelheight")
        self.gridLayout.addWidget(self.labelheight, 1, 4, 1, 1)
        self.y0 = QtWidgets.QSpinBox(self.frameGeometry)
        self.y0.setObjectName("y0")
        self.gridLayout.addWidget(self.y0, 3, 1, 1, 1)
        self.width = QtWidgets.QSpinBox(self.frameGeometry)
        self.width.setMinimum(16)
        self.width.setMaximum(1280)
        self.width.setSingleStep(16)
        self.width.setProperty("value", 1280)
        self.width.setObjectName("width")
        self.gridLayout.addWidget(self.width, 3, 3, 1, 1)
        self.labelx0 = QtWidgets.QLabel(self.frameGeometry)
        self.labelx0.setObjectName("labelx0")
        self.gridLayout.addWidget(self.labelx0, 1, 0, 1, 1)
        self.labelwidth = QtWidgets.QLabel(self.frameGeometry)
        self.labelwidth.setObjectName("labelwidth")
        self.gridLayout.addWidget(self.labelwidth, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.frameGeometry)
        self.frameExposure.raise_()
        self.frameFlip.raise_()
        self.frameGeometry.raise_()
        self.frameGamma.raise_()
        self.frameMode.raise_()
        self.gainLabel.setBuddy(self.gain)
        self.labelblacklevel.setBuddy(self.blacklevel)
        self.exposureLabel.setBuddy(self.exposure)
        self.labelgamma.setBuddy(self.gamma)
        self.labelsharpness.setBuddy(self.sharpness)
        self.labelVideoMode.setBuddy(self.videomode)
        self.labelFrameRate.setBuddy(self.framerate)
        self.labely0.setBuddy(self.y0)
        self.labelheight.setBuddy(self.height)
        self.labelx0.setBuddy(self.x0)
        self.labelwidth.setBuddy(self.width)

        self.retranslateUi(QSpinnakerWidget)
        QtCore.QMetaObject.connectSlotsByName(QSpinnakerWidget)
        QSpinnakerWidget.setTabOrder(self.exposure, self.autoexposure)
        QSpinnakerWidget.setTabOrder(self.autoexposure, self.gain)
        QSpinnakerWidget.setTabOrder(self.gain, self.autogain)
        QSpinnakerWidget.setTabOrder(self.autogain, self.blacklevel)
        QSpinnakerWidget.setTabOrder(self.blacklevel, self.gamma)
        QSpinnakerWidget.setTabOrder(self.gamma, self.sharpness)
        QSpinnakerWidget.setTabOrder(self.sharpness, self.videomode)
        QSpinnakerWidget.setTabOrder(self.videomode, self.framerate)
        QSpinnakerWidget.setTabOrder(self.framerate, self.x0)
        QSpinnakerWidget.setTabOrder(self.x0, self.y0)
        QSpinnakerWidget.setTabOrder(self.y0, self.width)
        QSpinnakerWidget.setTabOrder(self.width, self.height)

    def retranslateUi(self, QSpinnakerWidget):
        _translate = QtCore.QCoreApplication.translate
        QSpinnakerWidget.setWindowTitle(_translate("QSpinnakerWidget", "QSpinnakerWidget"))
        QSpinnakerWidget.setStatusTip(_translate("QSpinnakerWidget", "Control Spinnaker camera"))
        self.mirrored.setStatusTip(_translate("QSpinnakerWidget", "Camera: Flip image around vertical axis"))
        self.mirrored.setText(_translate("QSpinnakerWidget", "&Mirrored"))
        self.flipped.setStatusTip(_translate("QSpinnakerWidget", "Camera: Flip image about horizontal axis"))
        self.flipped.setText(_translate("QSpinnakerWidget", "&Flipped"))
        self.gainLabel.setText(_translate("QSpinnakerWidget", "&Gain"))
        self.autogain.setStatusTip(_translate("QSpinnakerWidget", "Camera: Optimize gain"))
        self.autogain.setText(_translate("QSpinnakerWidget", "Auto"))
        self.gain.setStatusTip(_translate("QSpinnakerWidget", "Camera gain"))
        self.gain.setSuffix(_translate("QSpinnakerWidget", " dB"))
        self.labelblacklevel.setText(_translate("QSpinnakerWidget", "Black Level"))
        self.blacklevel.setStatusTip(_translate("QSpinnakerWidget", "Camera black level"))
        self.blacklevel.setSuffix(_translate("QSpinnakerWidget", " %"))
        self.exposure.setStatusTip(_translate("QSpinnakerWidget", "Camera exposure time "))
        self.exposure.setSuffix(_translate("QSpinnakerWidget", " μs"))
        self.exposureLabel.setText(_translate("QSpinnakerWidget", "&Exposure Time"))
        self.autoexposure.setStatusTip(_translate("QSpinnakerWidget", "Camera: Optimize exposure time"))
        self.autoexposure.setText(_translate("QSpinnakerWidget", "Auto"))
        self.labelgamma.setText(_translate("QSpinnakerWidget", "Gamma"))
        self.labelsharpness.setText(_translate("QSpinnakerWidget", "Sharpness"))
        self.gamma.setStatusTip(_translate("QSpinnakerWidget", "Camera gamma"))
        self.sharpness.setStatusTip(_translate("QSpinnakerWidget", "Camera sharpness"))
        self.labelVideoMode.setText(_translate("QSpinnakerWidget", "Video Mode"))
        self.labelFrameRate.setText(_translate("QSpinnakerWidget", "Frame &Rate"))
        self.videomode.setStatusTip(_translate("QSpinnakerWidget", "Camera video mode"))
        self.videomode.setItemText(0, _translate("QSpinnakerWidget", "Mode 0"))
        self.videomode.setItemText(1, _translate("QSpinnakerWidget", "Mode 1"))
        self.videomode.setItemText(2, _translate("QSpinnakerWidget", "Mode 2"))
        self.videomode.setItemText(3, _translate("QSpinnakerWidget", "Mode 3"))
        self.videomode.setItemText(4, _translate("QSpinnakerWidget", "Mode 4"))
        self.videomode.setItemText(5, _translate("QSpinnakerWidget", "Mode 5"))
        self.videomode.setItemText(6, _translate("QSpinnakerWidget", "Mode 6"))
        self.videomode.setItemText(7, _translate("QSpinnakerWidget", "Mode 7"))
        self.framerate.setStatusTip(_translate("QSpinnakerWidget", "Camera frame rate"))
        self.framerate.setSuffix(_translate("QSpinnakerWidget", " Hz"))
        self.labely0.setText(_translate("QSpinnakerWidget", "&y0"))
        self.x0.setStatusTip(_translate("QSpinnakerWidget", "Camera ROI: bottom left corner"))
        self.height.setStatusTip(_translate("QSpinnakerWidget", "Camera ROI: height"))
        self.labelheight.setText(_translate("QSpinnakerWidget", "&Height"))
        self.y0.setStatusTip(_translate("QSpinnakerWidget", "Camera ROI: bottom left corner"))
        self.width.setStatusTip(_translate("QSpinnakerWidget", "Camera ROI: width"))
        self.labelx0.setText(_translate("QSpinnakerWidget", "&x0"))
        self.labelwidth.setText(_translate("QSpinnakerWidget", "&Width"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QSpinnakerWidget = QtWidgets.QFrame()
    ui = Ui_QSpinnakerWidget()
    ui.setupUi(QSpinnakerWidget)
    QSpinnakerWidget.show()
    sys.exit(app.exec_())

