
import Vehical

class VehicalManager:

	cars = {}

	def __init__():
		pass
		
	def addCar(name, ip, port, control, navigation):
		cars[name] = (Vehical(name, ip, port, control, navigation))
		
	def removeCar(name):
		cars.pop(name)
		
	def connect(name):
		try:
			self.cars[name].interface.connectToHost()
			return True
		except (ConnectionError, OSError) as e:
			return False
			
	def disconnect(name):
		self.cars[name].interface.disconnectFromHost()
		
	def sendMsg(direction, speed):
		try:
			self.cars[name].interface.sendMsg(direction, speed)
			return True
		except (ConnectionError, OSError) as e:
			return False