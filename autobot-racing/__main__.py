import queue
from EthernetInterface import EthernetInterface
from UIManager import UIManager
from cv.ComputerVision import *
import threading
from MessageQueue import MessageQueue


class FrameworkManager():
	##-----------------------------------------------------------------------------
	## Constructor
	##-----------------------------------------------------------------------------
	def __init__(self):
		self._run = True
	
		# Create message queues.
		self.telemetryQueue = queue.Queue()
		self.UIQueue = MessageQueue(self)

	
		# Set up components.
		self.cv = ComputerVision(self, -1)
		self.UserInterface = UIManager(self)
		self.EthernetInterface = EthernetInterface(self)
		self.carList = [] #Stores all car objects

	##-----------------------------------------------------------------------------
	## Start the program.
	##-----------------------------------------------------------------------------
	def run(self):
		tUI = threading.Thread(target=self.UserInterface.openCarStatsUI)
		tCV = threading.Thread(target=self.cv.run, args=(False,))
		tCV.daemon = True
		tUI.daemon = True
		tUI.start()
		tCV.start()
		
		# Program main loop.
		try:
			while self._run:
				self.getLatestTelemetry()
		except KeyboardInterrupt as e:
			exit(0)
	
	# Pulls the latest telemetry from the telemetry queue.
	def getLatestTelemetry(self):
		try:
			(position, heading, color) = self.telemetryQueue.get(True, 1)
			print("VEHICLE WITH COLOR " + str(color) + " DETECTED AT " + str(position) + " IN DIRECTION " + str(heading))
		except queue.Empty:
			pass

##Car Methods-----------------------------------------------------------------------------------------------------------------------------------------
	##-----------------------------------------------------------------------------
	## Returns the current list of cars
	##-----------------------------------------------------------------------------
	def getCarList(self):
		return self.carList

	##-----------------------------------------------------------------------------
	## Updates the list of cars
	##-----------------------------------------------------------------------------
	def updateCarList(self, newList):
		self.carList = newList
		print(len(self.carList))
##----------------------------------------------------------------------------------------------------------------------------------------------------


##UI Methods------------------------------------------------------------------------------------------------------------------------------------------
	##-----------------------------------------------------------------------------
	## Updates the list of cars
	##-----------------------------------------------------------------------------
	def updateCarFrameColor(self, carName, status):
		self.UserInterface.changeCarFrameColor(carName, status)

	##-----------------------------------------------------------------------------
	## Gets the a list of Control Systems
	##-----------------------------------------------------------------------------
	def getControlSystems(self):
		return ['Option 1', 'Option 2']

	##-----------------------------------------------------------------------------
	## Gets the a list of Guidance Systems
	##-----------------------------------------------------------------------------
	def getGuidanceSystems(self):
		return ['Option 1', 'Option 2']

##----------------------------------------------------------------------------------------------------------------------------------------------------



##EthernetInterface Functions-------------------------------------------------------------------------------------------------------------------------
	##-----------------------------------------------------------------------------
	## Connects to the PI of the newly added car
	##-----------------------------------------------------------------------------
	def connectNewCar(self, car):
		self.EthernetInterface.connectToPI(car)

	##-----------------------------------------------------------------------------
	## Updates the connection of the specified car
	##-----------------------------------------------------------------------------
	def updateCarConnection(self, car):
		self.EthernetInterface.updateConnection(car)

	##-----------------------------------------------------------------------------
	## Disconnects from the specified car
	##-----------------------------------------------------------------------------
	def removeConnection(self, car):
		self.EthernetInterface.disconnectFromPI(car)
##----------------------------------------------------------------------------------------------------------------------------------------------------

#}

if __name__ == "__main__":
	manager = FrameworkManager()
	manager.run()
