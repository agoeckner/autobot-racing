from collections import deque

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
		self.controlSystem = controlSystem
		self.guidanceSystem = guidanceSystem
		self.interface = PCConnection(carName, IP, port)
		
		# Store the most recent position/heading data.
		self.position = deque(maxlen = self.POSITION_HISTORY_POINTS)
		self.heading = deque(maxlen = self.HEADING_HISTORY_POINTS)