import queue
from EthernetInterface import EthernetInterface
from UIManager import UIManager
from cv.ComputerVision import *

class FrameworkManager():
	##-----------------------------------------------------------------------------
	## Constructor
	##-----------------------------------------------------------------------------
	def __init__(self):
		# Create message queues.
		self.telemetryQueue = queue.Queue()
	
		# Set up components.
		self.cv = ComputerVision(self.telemetryQueue)
		self.UserInterface = UIManager(self)
		self.EthernetInterface = EthernetInterface(self)
		self.carList = [] #Stores all car objects

	##-----------------------------------------------------------------------------
	## Start the program.
	##-----------------------------------------------------------------------------
	def run(self):
		# TODO: Isn't the UI a separate thread?
		# self.UserInterface.openCarStatsUI()
		
		# TODO: Start computer vision system in a separate thread.
		# self.cv.run()
		
		# Program main loop.
		while True:
			self.getLatestTelemetry()
	
	# Pulls the latest telemetry from the telemetry queue.
	def getLatestTelemetry():
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
