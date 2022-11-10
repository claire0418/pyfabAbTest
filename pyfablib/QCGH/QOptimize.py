
from .CGH import CGH
import numpy as np
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
from pyfablib.traps.QTrapGroup import QTrapGroup as group

class QOptimize(CGH):

    calculate = pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs): 
        super(QOptimize, self).__init__(*args, **kwargs)

        self.Vm = []
        self.delta = []
	
        self._cameraPitch = 4.8
        self._slmPitch = 11.1
        self.xc = 946
        self.yc = 839
        self.xs = 434
        self.ys = 306
        self.zc = 0
        self.phis = 9.8
        self._wavelength = 0.532
        self._focalLength = 200
        self._thetac = -89.3
        self.scaleFactor = 28.22
        self.magnification = 60
        self.refractiveIndex = 1.47

    def calculate_delta(self, trap):
        '''calculate delta_mj for one trap'''
        theta = np.radians(self._thetac)
        xi = (trap.x-self.xc) * self._cameraPitch/self.magnification*self.refractiveIndex
        yi = (trap.y-self.yc) * self._cameraPitch/self.magnification*self.refractiveIndex
        zi = (trap.z-self.zc) * self._cameraPitch/self.magnification*self.refractiveIndex
	
        xm = np.cos(theta)*xi - np.sin(theta)*yi
        ym = np.cos(theta)*yi + np.sin(theta)*xi
        zm = zi

        deltam = np.zeros(self.shape)
        y = -(np.arange(0,self.shape[0])-self.ys)*self._slmPitch/self.scaleFactor
        alpha = np.cos(np.radians(self.phis))
        x = (np.arange(0,self.shape[1])-self.xs)*alpha*self._slmPitch/self.scaleFactor
        i, j = np.meshgrid(x,y)
	
        deltam = (np.pi*zm/(self._wavelength*(self._focalLength**2)))*(i**2 + j**2) \
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
            e = np.full(self.shape,np.e)
            v = (1/(self.shape[0]*self.shape[1]))*np.power(e,1j*(phase-d))
            self.Vm.append(sum(sum(v)))

    def Vm_avg(self):
        Vm = np.array(self.Vm)
        return sum(abs(Vm))/len(Vm)

    def phi_init(self,delta):
        e = np.full(self.shape,np.e)
        psi = np.zeros(self.shape,dtype='complex_')
        for m in range(len(delta)):
            #random = 2*np.pi*np.random.rand(self.shape[0], self.shape[1])
            psi += np.power(e,1j*(delta[m]))
        phi = np.angle(psi)
        return phi  

    def optimize(self,traps):
	
        self.delta.clear()
        iterations = np.arange(0,15)
        self.compile_delta(traps)
        delta = np.array(self.delta)
        self.recalculate_Vm(self.phi_init(delta), traps)
        Vm = np.array(self.Vm)

        structure = []
        for trap in traps:
            structure.append(trap.structure)
        w = np.ones(len(Vm))
        psi = np.zeros((len(Vm),self.shape[0], self.shape[1]), dtype='complex_')
        e = np.full(self.shape,np.e) 
	
        for k in iterations:
            for m in range(0,len(Vm)):
                w[m] = w[m]*(self.Vm_avg()/abs(Vm[m]))
                psi[m] = np.power(e,1j*delta[m])*w[m]*(Vm[m]/abs(Vm[m]))
            phi = np.angle(sum(psi))
            self.recalculate_Vm(phi, traps)
            Vm = np.array(self.Vm)
        for m in range(0,len(Vm)):
            if structure[m] is not None:
                psi[m] = psi[m]*structure[m]
        phi = np.angle(sum(psi))
        phi_final = ((128. / np.pi) * phi + 127.).astype(np.uint8)
        self.calculate.emit(phi_final)
