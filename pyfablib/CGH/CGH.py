#!/usr/bin/env python

"""CGH.py: compute phase-only holograms for optical traps."""

import numpy as np
from PyQt4 import QtGui, QtCore
from numba import jit
import json
from time import time


class CGH(QtCore.QObject):
    """Base class for computing computer-generated holograms.

    For each trap, the coordinate r obtained from the fabscreen
    is measured relative to the calibrated location rc of the
    zeroth-order focal point, which itself is measured relative to
    the center of the focal plane. The resulting displacement is
    projected onto the coordinate system in the SLM place.
    Projection involves a calibrated rotation about z with
    a rotation matrix m.

    The hologram is computed using calibrated wavenumbers for
    the Cartesian coordinates in the SLM plane.  These differ from
    each other because the SLM is likely to be tilted relative to the
    optical axis.

    NOTES:
    This version calls QtGui.qApp.processEvents() after computing
    each trap's holograms.  This keeps the GUI responsive, but is
    ugly and slows the CGH computation.  It would be better to
    move CGH into its own thread, or at least to push the computation
    into its own thread.
    """

    sigComputing = QtCore.pyqtSignal(bool)
    sigHologramReady = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, slm=None):
        super(CGH, self).__init__()
        self.traps = []
        # SLM geometry
        self.slm = slm
        self.w = self.slm.width()
        self.h = self.slm.height()

        # Conversion from SLM pixels to wavenumbers
        self._qpp = 2. * np.pi / self.w / 10.
        # Effective aspect ratio of SLM pixels
        self._alpha = 1.
        # Location of optical axis in SLM coordinates
        self._rs = QtCore.QPointF(self.w / 2., self.h / 2.)
        self.updateGeometry()

        # Coordinate transformation matrix for trap locations
        self.m = QtGui.QMatrix4x4()
        # Location of optical axis in camera coordinates
        self._rc = QtGui.QVector3D(320., 240., 0.)
        # Orientation of camera relative to SLM
        self._theta = 0.
        self.updateTransformationMatrix()
        # Splay wavenumber
        self._k0 = 0.01

    @QtCore.pyqtSlot(object, object)
    def setProperty(self, name, value):
        setattr(self, name, value)

    @QtCore.pyqtSlot(object)
    def setTraps(self, traps):
        self.traps = traps
        self.compute()

    @jit(parallel=True)
    def quantize(self, psi):
        phi = ((128. / np.pi) * np.angle(psi) + 127.).astype(np.uint8)
        return phi.T

    @jit(parallel=True)
    def compute_one(self, amp, r, buffer):
        """Compute phase hologram to displace a trap with
        a specified complex amplitude to a specified position
        """
        ex = np.exp(self.iqx * r.x() + self.iqxsq * r.z())
        ey = np.exp(self.iqy * r.y() + self.iqysq * r.z())
        np.outer(amp * ex, ey, buffer)

    def window(self, r):
        x = 0.5 * np.pi * np.array([r.x() / self.w, r.y() / self.h])
        fac = 1. / np.prod(np.sinc(x))
        return np.min((np.abs(fac), 100.))

    @jit(parallel=True)
    def compute(self, all=False):
        """Compute phase hologram for specified traps
        """
        self.sigComputing.emit(True)
        start = time()
        self._psi.fill(0. + 0j)
        for trap in self.traps:
            if ((all is True) or
                    (trap.state == trap.state.selected) or
                    (trap.psi is None)):
                r = self.m * trap.r
                # experimental splay calculation
                fac = 1./(1. + self.k0 * (r.z() - self.rc.z()))
                r *= QtGui.QVector3D(fac, fac, 1.)
                amp = trap.amp * self.window(r)
                if trap.psi is None:
                    trap.psi = self._psi.copy()
                self.compute_one(amp, r, trap.psi)
            self._psi += trap.psi
            # QtGui.qApp.processEvents()
            # QtGui.qApp.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
        # self.slm.data = self.quantize(self._psi)
        self.sigHologramReady.emit(self.quantize(self._psi))
        self.time = time() - start
        self.sigComputing.emit(False)

    def outertheta(self, x, y):
        return np.arctan2.outer(y, x)

    def updateGeometry(self):
        """Compute position-dependent properties in SLM plane
        and allocate buffers.
        """
        shape = (self.w, self.h)
        self._psi = np.zeros(shape, dtype=np.complex_)
        qx = np.arange(self.w) - self.rs.x()
        qy = np.arange(self.h) - self.rs.y()
        qx = self._qpp * qx
        qy = self._alpha * self._qpp * qy
        self.iqx = 1j * qx
        self.iqy = 1j * qy
        self.iqxsq = 1j * qx * qx
        self.iqysq = 1j * qy * qy
        self.itheta = 1j * self.outertheta(qx, qy)

    @property
    def xs(self):
        return self.rs.x()

    @xs.setter
    def xs(self, xs):
        rs = self.rs
        rs.setX(xs)
        self.rs = rs

    @property
    def ys(self):
        return self.rs.y()

    @ys.setter
    def ys(self, ys):
        rs = self.rs
        rs.setY(ys)
        self.rs = rs

    @property
    def rs(self):
        return self._rs

    @rs.setter
    def rs(self, rs):
        if isinstance(rs, QtCore.QPointF):
            self._rs = rs
        else:
            self._rs = QtCore.QPointF(rs[0], rs[1])
        self.updateGeometry()
        self.compute(all=True)

    @property
    def qpp(self):
        return self._qpp * 1000.

    @qpp.setter
    def qpp(self, qpp):
        self._qpp = float(qpp) / 1000.
        self.updateGeometry()
        self.compute(all=True)

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = float(alpha)
        self.updateGeometry()
        self.compute(all=True)

    def updateTransformationMatrix(self):
        self.m.setToIdentity()
        self.m.rotate(self.theta, 0., 0., 1.)
        self.m.translate(-self.rc)

    @property
    def xc(self):
        return self.rc.x()

    @xc.setter
    def xc(self, xc):
        rc = self.rc
        rc.setX(xc)
        self.rc = rc

    @property
    def yc(self):
        return self.rc.y()

    @yc.setter
    def yc(self, yc):
        rc = self.rc
        rc.setY(yc)
        self.rc = rc

    @property
    def zc(self):
        return self.rc.z()

    @zc.setter
    def zc(self, zc):
        rc = self.rc
        rc.setZ(zc)
        self.rc = rc

    @property
    def rc(self):
        return self._rc

    @rc.setter
    def rc(self, rc):
        if isinstance(rc, QtGui.QVector3D):
            self._rc = rc
        else:
            self._rc = QtGui.QVector3D(rc[0], rc[1], rc[2])
        self.updateTransformationMatrix()
        self.compute(all=True)

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, theta):
        self._theta = float(theta)
        self.updateTransformationMatrix()
        self.compute(all=True)

    @property
    def k0(self):
        return self._k0

    @k0.setter
    def k0(self, k0):
        self._k0 = float(k0)
        self.compute(all=True)

    @property
    def calibration(self):
        return {'qpp': self.qpp,
                'alpha': self.alpha,
                'rs': (self.rs.x(), self.rs.y()),
                'rc': (self.rc.x(), self.rc.y(), self.rc.z()),
                'theta': self.theta,
                'kx0': self.kx0,
                'ky0': self.ky0}

    @calibration.setter
    def calibration(self, values):
        if not isinstance(values, dict):
            return
        for attribute, value in values.iteritems():
            print(attribute, value)
            try:
                setattr(self, attribute, value)
            except AttributeError:
                print('unknown attribute:', attribute)

    def serialize(self):
        return json.dumps(self.calibration,
                          indent=2,
                          separators=(',', ': '),
                          ensure_ascii=False)

    def deserialize(self, s):
        values = json.loads(s)
        self.calibration = values
