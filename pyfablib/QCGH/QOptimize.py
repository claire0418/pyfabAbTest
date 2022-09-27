# intensity optimization algorithm for point trap
# later: phase stuff and also traps of diff shapes

from .CGH import CGH
import numpy as np
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
from pyfablib.traps.QTrapGroup import QTrapGroup as group

class QOptimize(CGH):

    recalculate = pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs): 
        super(QOptimize, self).__init__(*args, **kwargs)

        self.Vm = []
        self.delta = []
        self.phi = np.zeros(self.shape)
	
    def getPhi(self,phi):
        self.phi = phi


    def calculate_delta(self, trap):
        '''calculate delta_mj for one trap'''
	
        xm = trap.x
        ym = trap.y
        zm = trap.z
	
        #SLM pixel coordinates, this might be wrong????
        #alpha = np.cos(np.radians(self.phis))
        #x = alpha*(np.arange(self.width) - self.xs)
        #y = np.arange(self.height) - self.ys

        deltam = np.zeros(self.shape)
        for x in range(0,self.height):
            for y in range(0,self.width):
                deltam[x][y] = (np.pi*zm/(self._wavelength*self._focalLength**2))*(x**2 + y**2)*(self._slmPitch**2)*self._cameraPitch \
                             + (np.pi*2/(self._wavelength*self._focalLength))*(x*xm + y*ym)*self._slmPitch*self._cameraPitch
        return deltam

    def compile_delta(self, traps):
        for trap in traps:
            d = self.calculate_delta(trap)
            self.delta.append(d)
	
    def recalculate_Vm(self, phase, traps):
        self.Vm.clear()
        for trap in traps:
            d = self.calculate_delta(trap)
            v = np.zeros(self.shape)
            for x in range(0,self.height):
                for y in range(0,self.width):
                    v[x][y] = (1/307200)*np.exp(1j*(phase[x][y]-d[x][y]))
            self.Vm.append(sum(sum(v)))

    def Vm_avg(self):
        Vm = np.array(self.Vm)
        return sum(abs(Vm))/len(Vm)

    def optimize(self,traps):
        iterations = np.arange(0,5)
        self.recalculate_Vm(self.phi, traps)
        self.compile_delta(traps)
        Vm = np.array(self.Vm)
        delta = np.array(self.delta)

        w = np.ones(len(Vm))
        phi = np.zeros(self.shape)

        for k in iterations:
            for m in range(0,len(Vm)):
                w[m] = w[m]*(self.Vm_avg()/abs(Vm[m]))
                for x in range(0,self.height):
                    for y in range(0,self.width):
                        phi[x][y] += np.angle(np.exp(1j*delta[m][x][y]*w[m])*(Vm[m]/abs(Vm[m])))
            self.recalculate_Vm(phi, traps)
				
        self.recalculate.emit(phi)
