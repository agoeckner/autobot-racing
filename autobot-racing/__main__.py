from EthernetInterface import EthernetInterface
from MessageQueue import MessageQueue
from UIManager import UIManager
from Vehicle import Vehicle
from VehicleManager import VehicleManager
from cv.ComputerVision import *
import controls as ngc
import inspect
import queue
import threading

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
	
		# Get list of control/guidance systems.
		self.controlSystems = self.getControlSystemObjects()
		self.guidanceSystems = self.getGuidanceSystemObjects()
		
	
		# Create message queues.
		self.telemetryQueue = queue.Queue()
		self.UIQueue = MessageQueue(self)

		# Set up components.
		self.cv = ComputerVision(self, -1)
		self.UserInterface = UIManager(self)
		self.vehicles = VehicleManager(self)
		
		# TODO: ADD A BOGUS TRACK
		self.track = Track([(100, 100), (100, 200), (200, 200), (200, 100), (100, 100)], [])

	##-----------------------------------------------------------------------------
	## Start the program.
	##-----------------------------------------------------------------------------
	def run(self):
		tUI = threading.Thread(target=self.UserInterface.openCarStatsUI)
		tCV = threading.Thread(target=self.cv.run, args=(False,))
		tQueue = threading.Thread(target=self.UIQueue.workerUI)
		tCV.daemon = True
		tUI.daemon = True
		tQueue.daemon = True
		tUI.start()
		tCV.start()
		tQueue.start()
		
		# Program main loop.
		try:
			while True:
				self.getLatestTelemetry()
				self.runNavGuidanceControl()
		except KeyboardInterrupt as e:
			exit(0)
	
	# Pulls the latest telemetry from the telemetry queue.
	def getLatestTelemetry(self):
		try:
			while True:
				(position, heading, color) = self.telemetryQueue.get(True, 1)
				
				vehicle = self.vehicles.getVehicleByColor(color)
				if vehicle != None:
					vehicle.position.append(position)
					vehicle.heading.append(heading)
			
		except queue.Empty:
			pass
	
	def runNavGuidanceControl(self):
		vehicles = self.vehicles.getList()
		for vehicle in vehicles:
		
			# Determine guidance.
			desiredHeading = vehicle.guidance.getDesiredHeading(vehicle.position[0])
			# desiredSpeed = vehicle.guidance.getDesiredSpeed(vehicle.position)
			
			# Run control algorithm.
			deltaHeading = vehicle.control.heading(vehicle.heading[0], desiredHeading)
			# deltaSpeed = vehicle.control.throttle(vehicle.speed, desiredSpeed)
			
			# Send commands to vehicle.
			vehicle.updateHeading(deltaHeading)
			hdg = vehicle.heading[0]
			# Snap to trinary, the only steering available on these cars.
			if hdg < 0: hdg = -1
			elif hdg > 0: hdg = 1
			# TODO: hardcoded speed
			vehicle.sendMsg(hdg, 1)
			# vehicle.updateSpeed(deltaSpeed)

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
		names = []
		for name, obj in inspect.getmembers(ngc):
			if inspect.isclass(obj) and "Control" in name:
				print("CONTROL SYSTEM FOUND: " + str(name) + " (" + str(obj) + ")")
				names.append(name)
		return names
	
	def getControlSystemObjects(self):
		objs = []
		for name, obj in inspect.getmembers(ngc):
			if inspect.isclass(obj) and "Control" in name:
				objs.append(obj)
		return objs

	##-----------------------------------------------------------------------------
	## Gets the a list of Guidance Systems
	##-----------------------------------------------------------------------------
	def getGuidanceSystems(self):
		names = []
		for name, obj in inspect.getmembers(ngc):
			if inspect.isclass(obj) and "Guidance" in name:
				print("GUIDANCE SYSTEM FOUND: " + str(name) + " (" + str(obj) + ")")
				names.append(name)
		return names
	def getGuidanceSystemObjects(self):
		objs = []
		for name, obj in inspect.getmembers(ngc):
			if inspect.isclass(obj) and "Guidance" in name:
				objs.append(obj)
		return objs

##----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	manager = FrameworkManager()
	manager.run()
