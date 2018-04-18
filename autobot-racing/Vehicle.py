from collections import deque
from EthernetInterface import EthernetInterface
import sys
import numpy as np

import controls as ngc

#Car class to store car objects
class Vehicle():
	POSITION_HISTORY_POINTS = 10
	HEADING_HISTORY_POINTS = 10
	
	# The maximum amount of time that a vehicle may be "missing" before stop command is sent.
	EMERGENCY_STOP_TIMEOUT = 2 #seconds

	def __init__(self, parent, name, IP, port, carFrameID, frame, controlSystem, guidanceSystem):
		
		# Set up parameters.
		self.parent = parent
		self.name = name
		self.color = (0, 0, 0)
		self.IP = IP
		self.port = port
		self.carFrameID = carFrameID
		self.frame = frame
		
		# Get the actual control system class.
		# print("Got control system: " + str(controlSystem))
		# self.control = parent.parent.controlSystems[controlSystem]
		# print("Vehicle " + str(name) + " using control system: " + str(self.control))
		# self.guidance = parent.parent.guidanceSystems[guidanceSystem]
		# print("Vehicle " + str(name) + " using guidance system: " + str(self.guidance))
		
		self.control = ngc.ControlSystem()
		self.guidance = ngc.WallFollowingGuidanceSystem(self.parent.parent,
			wallDistance = 20, lookahead = 100)
		
		self.interface = EthernetInterface(name, IP, port)
		
		# Get colors... This is ugly.
		if name.upper() == "RED":
			self.color = (255, 0, 0)
		elif name.upper() == "GREEN":
			self.color = (0, 255, 0)
		elif name.upper() == "BLUE":
			self.color = (0, 0, 255)
		
		# Store the most recent position/heading data.
		self.position = deque(maxlen = self.POSITION_HISTORY_POINTS)
		self.heading = deque(maxlen = self.HEADING_HISTORY_POINTS)
		
		# These variables store the desired heading/speed.
		# AKA, the output of the guidance system.
		self.desiredHeading = 0.0
		self.desiredSpeed = 0
		
		# These variables store the current, filtered telemetry data.
		# AKA, the output of the Kalman Filter.
		self.actualHeading = 0.0
		self.actualPosition = (0.0, 0.0)
		self.actualSpeed = 0
		
		# Add dummy initial data.
		self.lastTelemetryTime = None
		# self.position.append((0,0))
		# self.heading.append(0)
		
		# Connect to Pi.
		if self.connect():
			print("Vehicle \"" + str(self.name) + "\" connected to transmitter.")
		else:
			print("WARN: Vehicle \"" + str(self.name) + "\" failed to connect to transmitter!")	

	def connect(self):
		try:
			self.interface.connectToHost()
			return True
		except (ConnectionError, OSError) as e:
			return False
			
	def disconnect(self):
		self.interface.disconnectFromHost()
		
	def sendMsg(self, direction, speed):
		try:
			self.interface.sendMsg(direction, speed)
			return True
		except (ConnectionError, OSError) as e:
			return False
	
	def updateTelemetry(self, position, heading):
		# Add to the telemetry history.
		self.position.append(positon)
		self.heading.append(heading)
		
		# Get the latest time.
		currentTime = time.time()
		deltaTime = currentTime - vehicle.lastTelemetryTime
		
		# Calculate vehicle speed.
		deltaPos = abs(numpy.linalg.norm(np.array(self.position[1]) - \
			np.array(position)))
		self.actualSpeed = deltaPos / deltaTime
		
		# Update last telemetry time.
		vehicle.lastTelemetryTime = currentTime
	
	def runNavGuidanceControl(self):
		# Automatically stop if we have no received telemetry recently.
		ltt = self.lastTelemetryTime
		if ltt != None and (time.time() - ltt) >= self.EMERGENCY_STOP_TIMEOUT:
			self.sendMsg(0, 0.0)
			print("WARN: Vehicle " + str(self.name) + " has been stopped.")
			continue
		
		# Determine guidance.
		desiredHeading = self.guidance.getDesiredHeading(self.actualPosition)
		desiredSpeed = self.guidance.getDesiredSpeed(self.actualPosition)
		
		# Run control algorithm.
		deltaHeading = self.control.heading(self.actualHeading, desiredHeading)
		deltaSpeed = self.control.throttle(self.speed, desiredSpeed)
		
		# Update the desired speed/heading values.
		self.updateHeading(deltaHeading)
		self.updateSpeed(deltaSpeed)
		
		# Snap steering  to trinary, the only steering available on these cars.
		hdg = self.desiredHeading
		if hdg < 0.0:
			# print("TURN LEFT?")
			hdg = -1
		elif hdg > 0.0:
			# print("TURN RIGHT?")
			hdg = 1
		else:
			hdg = 0
			
		# TEMPORARY INVERSE
		# hdg = -hdg
		
		# Send command to the car.
		self.sendMsg(hdg, self.desiredSpeed)
	
	def updateHeading(self, deltaHeading):
		self.desiredHeading += deltaHeading
	
	def updateSpeed(self, deltaSpeed):
		self.desiredSpeed += deltaSpeed
