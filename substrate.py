from core import *
from numa import *
from bus import *


class SubstrateModel:
	def __init__(self):
		self.numaList = []
		self.busList = []

	def createNumas(self, nrNumas, nrCores):
		initMemoryCapacity = 50
		initCPU = 10
		for k in range(nrNumas):
			numaID = str(k)
			n = NUMA(numaID, initMemoryCapacity)
			for i in range(nrCores):
				coreID = str(k) + "_" + str(i)
				c = Core(coreID, initCPU, n)
				n.coreList.append(c)
			self.numaList.append(n)

	def createBuses(self):
		busCapacity = 5
		for k in range(len(self.numaList)-2):
			b = Bus(self.numaList[k], self.numaList[k+1], busCapacity)
			self.busList.append(b)


	def populate(self):
		nrNumas = 2
		nrCores = 4
		nrBuses = 1

		self.createNumas(nrNumas, nrCores)
		self.createBuses()	

	def getTotalMemory(self):
		total = 0
		for numa in self.numaList:
			total += numa.memoryCapacity
		return total

	def getTotalCPU(self):
		total = 0
		for numa in self.numaList:
			for cpu in numa.coreList:
				total += cpu.capacity
		return total

	def print(self):
		for numa in self.numaList:
			numa.print()

	def partition(self, sfc):
		for vnf in sfc.vnfList:
			assigned = False
			for numa in self.numaList:
				if numa.memoryCapacity >= vnf.memoryDemand: #if numa has enough memory
					for core in numa.coreList:
						if core.capacity >= vnf.cpuDemand:
							core.process(vnf)
							numa.processWithoutCoreAssignment(vnf)
							assigned = True
							break
					if assigned:
						break
			if not assigned:
				return False
		return True
