from collections import deque
from Communication import PCConnection

import controls as ngc

#Car class to store car objects
class Vehicle():
	POSITION_HISTORY_POINTS = 10
	HEADING_HISTORY_POINTS = 10

	def __init__(self, carName, IP, port, carFrameID, frame, lapNum, place, lapTimes, controlSystem, guidanceSystem):
		self.carName = carName
		self.IP = IP
		self.port = port
		self.carFrameID = carFrameID
		self.frame = frame
		self.lapNum = lapNum
		self.place = place
		self.lapTimes = lapTimes
		self.control = ngc.ControlSystem() #TODO: controlSystem
		self.guidance = ngc.WallFollowingGuidanceSystem(
					None,#TODO: TRACK HERE, self.track,
					wallDistance = 10,
					lookahead = 200) #TODO: guidanceSystem
		self.interface = PCConnection(carName, IP, port)
		
		# Store the most recent position/heading data.
		self.position = deque(maxlen = self.POSITION_HISTORY_POINTS)
		self.heading = deque(maxlen = self.HEADING_HISTORY_POINTS)

	def updateHeading(self, deltaHeading):
		print("UPDATE HEADING BY " + str(deltaHeading))

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