import queue
from EthernetInterface import EthernetInterface
from UIManager import UIManager
from cv.ComputerVision import *
import threading
from MessageQueue import MessageQueue
import controls as ngc
from Vehicle import Vehicle

#TODO: TEMPORARY!
class Track:
	def __init__(self, innerWall, outerWall):
		self.innerWall = innerWall
		self.outerWall = outerWall
		self.track = self


class FrameworkManager():
	##-----------------------------------------------------------------------------
	## Constructor
	##-----------------------------------------------------------------------------
	def __init__(self):
		# Create message queues.
		self.telemetryQueue = queue.Queue()
		self.UIQueue = MessageQueue(self)

		# Set up components.
		self.cv = ComputerVision(self, -1)
		self.UserInterface = UIManager(self)
		# self.EthernetInterface = EthernetInterface(self)
		self.carList = [] #Stores all car objects
		
		# TODO: ADD A BOGUS CAR
		self.track = Track([(100, 100), (100, 200), (200, 200), (200, 100), (100, 100)], [])
		veh = Vehicle(
			"TESTING",
			"128.10.120.200",
			4000,
			None,
			None,
			0,
			0,
			0,
			ngc.ControlSystem(),
			ngc.WallFollowingGuidanceSystem(self,
					wallDistance = 10,
					lookahead = 80)
			)
		self.carList.append(veh)
		if veh.connect():
			print("CONNECTED")
		else:
			print("CONNECTION FAILED")

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
			while True:
				self.getLatestTelemetry()
				# self.runNavGuidanceControl()
		except KeyboardInterrupt as e:
			exit(0)
	
	# Pulls the latest telemetry from the telemetry queue.
	def getLatestTelemetry(self):
		try:
			while True:
				(position, heading, color) = self.telemetryQueue.get(True, 1)
				
				# TODO, determine correct car based on color and then do this
				vehicle = self.carList[0]
				vehicle.position.append(position)
				vehicle.heading.append(heading)
			
		except queue.Empty:
			pass
	
	def runNavGuidanceControl(self):
		for vehicle in self.carList:
		
			# Determine guidance.
			desiredHeading = vehicle.guidance.getDesiredHeading(vehicle.position[0])
			# desiredSpeed = vehicle.guidance.getDesiredSpeed(vehicle.position)
			
			# Run control algorithm.
			deltaHeading = vehicle.control.heading(vehicle.heading[0], desiredHeading)
			# deltaSpeed = vehicle.control.throttle(vehicle.speed, desiredSpeed)
			
			# Send commands to vehicle.
			vehicle.updateHeading(deltaHeading)
			hdg = 0
			if hdg < 0: hdg = -1
			elif hdg > 0: hdg = 1
			# TODO: hardcoded speed
			vehicle.sendMsg(hdg, 1)
			# vehicle.updateSpeed(deltaSpeed)

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
