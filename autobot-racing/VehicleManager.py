
import Vehicle

class VehicleManager:

	cars = {}

	def __init__():
		pass
		
	def addCar(carName, IP, port, carFrameID, frame, lapNum, place, lapTimes, controlSystem, guidanceSystem):
		cars[carName] = Vehicle(carName, IP, port, carFrameID, frame, lapNum, place, lapTimes, controlSystem, guidanceSystem)
		
	def removeCar(carName):
		cars.pop(carName)
		
	def connect(carName):
		try:
			self.cars[carName].interface.connectToHost()
			return True
		except (ConnectionError, OSError) as e:
			return False
			
	def disconnect(carName):
		self.cars[carName].interface.disconnectFromHost()
		
	def sendMsg(carName, direction, speed):
		try:
			self.cars[carName].interface.sendMsg(direction, speed)
			return True
		except (ConnectionError, OSError) as e:
			return False