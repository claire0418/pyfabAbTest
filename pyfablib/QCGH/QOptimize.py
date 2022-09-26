# intensity optimization algorithm for point trap
# later: phase stuff and also traps of diff shapes

from .CGH import CGH
import numpy as np
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
from .traps.QTrapGroup import QTrapGroup as group

class QOptimize(CGH):

    phaseReady = pyqtSignal(np.ndarray)
    recalculate = pyqtSignal()

    def __init__(self, *args, **kwargs): 
        super(QOptimize, self).__init__(*args, **kwargs)

	self.Vm = []
	self.delta = []


    def calculate_delta(self, xm, ym, zm):
	'''calculate delta_mj for one trap'''

	#SLM pixel coordinates, this might be wrong????
	alpha = np.cos(np.radians(self.phis))
        x = alpha*(np.arange(self.width) - self.xs)
        y = np.arange(self.height) - self.ys

	deltam = np.zeros((480,640))
	for x in range(0,480):
		for y in range(0,640):
			deltam[x][y] = (np.pi*zm/(self._wavelength*self._focalLength**2))*(x**2 + y**2)*(self._slmPitch**2)*self._cameraPitch \
				     + (np.pi*2/(self._wavelength*self._focalLength))*(x*xm + y*ym)*self._slmPitch*self._cameraPitch
	return deltam

    def compile_delta(traps):
	for trap in traps:
	    d = calculate_delta(self, group.trap.r)
	    self.delta.append(d)
	
    def recalculate_Vm(phase, traps):
	self.Vm.clear()
	for trap in traps:
            d = calculate_delta(self, group.trap.r) #group.trap.r might not work hnnng
	    v = np.zeros((480,640))
	    for x in range(0,480):
		for y in range(0,640):
		    v[x][y] = (1/N)*np.exp(1j*(phase[x][y]-d[x][y])) #N ?????
	    self.Vm.append(sum(sum(v,[])))

    def Vm_avg():
	Vm = np.array(self.Vm)
	return sum(abs(Vm))/len(Vm)

    def optimize(traps):

	recalculate_Vm(self.phi, traps)
	compile_delta(traps)
	Vm = np.array(self.Vm)
	delta = np.array(self.delta)

	w = np.ones(len(Vm))
	phi = np.zeros((480,640))

	for k in range(0,5):
	    for m in range(0,len(Vm)):
		w[m] = w[m]*(Vm_avg()/abs(Vm[m])
		for x in range(0,480):
		    for y in range(0,640):
			phi[x][y] += np.angle(np.exp(1j*delta[m][x][y]*w[m])*(Vm[m]/abs(Vm[m])))
	    recalculate_Vm(phi, traps)
				
	self.recalculate.emit(phi)
