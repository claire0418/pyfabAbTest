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
	
        xm = (trap.x-self.xc) * self._cameraPitch
        ym = (trap.y-self.yc) * self._cameraPitch
        zm = (trap.z-self.zc) * self._cameraPitch #idk what's going on here
	
        #SLM pixel coordinates, this might be wrong????
        #alpha = np.cos(np.radians(self.phis))
        #x = alpha*(np.arange(self.width) - self.xs)
        #y = np.arange(self.height) - self.ys

        deltam = np.zeros(self.shape)
        for y in range(0,self.shape[0]):
            #j = (-y+self.shape[0]-self.ys)*self._slmPitch
            j = (y-self.ys)*self._slmPitch
            for x in range(0,self.shape[1]):
                alpha = np.cos(np.radians(self.phis))
                i = (x-self.xs)*alpha*self._slmPitch
                deltam[y][x] = (np.pi*zm/(self._wavelength*(self._focalLength**2)))*(i**2 + j**2) \
                             + (np.pi*2/(self._wavelength*self._focalLength))*(i*xm + j*ym)
        return deltam

    def compile_delta(self, traps):
        for trap in traps:
            d = self.calculate_delta(trap)
            self.delta.append(d)
	
    def recalculate_Vm(self, phase, traps):
        self.Vm.clear()
        for trap in traps:
            d = self.calculate_delta(trap)
            v = np.zeros(self.shape, dtype = 'complex_')
            for x in range(0,self.shape[0]):
                for y in range(0,self.shape[1]):
                    v[x][y] = (1/(self.shape[0]*self.shape[1]))*np.exp(1j*(phase[x][y]-d[x][y]))
            self.Vm.append(sum(sum(v)))

    def Vm_avg(self):
        Vm = np.array(self.Vm)
        return sum(abs(Vm))/len(Vm)

    def quantize(self, psi):
        return ((128. / np.pi) * (psi) + 127.).astype(np.uint8)

    def phi_init(self, delta):
        phi = np.zeros(self.shape)
        phi_m = np.zeros(self.shape, dtype = 'complex_')
        for m in range(0,len(delta)):
            random = 2*np.pi*np.random.rand()
            for x in range(0,self.shape[0]):
                for y in range(0,self.shape[1]):
                    phi_m[x][y] += np.exp(1j*(delta[x][y]+random))
        for x in range(0,self.shape[0]):
            for y in range(0,self.shape[1]):
                phi[x][y] = np.angle(phi_m[x][y])
        return phi
        
        

    def optimize(self,traps):
	
        iterations = np.arange(0,2)
        delta = np.array(self.delta)
        phi_init = self.phi_init(delta)
        self.recalculate_Vm(phi_init, traps)
        self.compile_delta(traps)
        Vm = np.array(self.Vm)


        w = np.ones(len(Vm))
        phi = np.zeros(self.shape)

        for k in iterations:
            for m in range(0,len(Vm)):
                w[m] = w[m]*(self.Vm_avg()/abs(Vm[m]))
                for x in range(0,self.shape[0]):
                    for y in range(0,self.shape[1]):
                        phi[x][y] += np.angle(np.exp(1j*delta[m][x][y]*w[m])*(Vm[m]/abs(Vm[m])))
            self.recalculate_Vm(phi, traps)
				
        phi_final = self.quantize(phi)
        self.recalculate.emit(phi_final)
