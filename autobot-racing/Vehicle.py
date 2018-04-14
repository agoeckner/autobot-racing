from collections import deque
from EthernetInterface import EthernetInterface
import sys

import controls as ngc

#Car class to store car objects
class Vehicle():
	POSITION_HISTORY_POINTS = 10
	HEADING_HISTORY_POINTS = 10

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
		self.headingGoal = 0.0
		
		# Add dummy initial data.
		self.lastTelemetryTime = None
		self.position.append((0,0))
		self.heading.append(0)
		
		# Connect to Pi.
		if self.connect():
			print("Vehicle \"" + str(self.name) + "\" connected to transmitter.")
		else:
			print("WARN: Vehicle \"" + str(self.name) + "\" failed to connect to transmitter!")

	def updateHeading(self, deltaHeading):
		self.headingGoal += deltaHeading
		# print("UPDATE HEADING BY " + str(deltaHeading))

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