from Vehicle import Vehicle

class VehicleManager:

	COLORS = [
		(255, 0, 0),
		(0, 255, 0),
		(0, 0, 255)]
	vehicleByColor = {}
	vehicleList = []

	def __init__(self):
		pass
		
	def addVehicle(self, vehicle):
		print("Added vehicle with name " + str(vehicle.name) + " and color " + str(vehicle.color))
		self.vehicleByColor[vehicle.color] = vehicle
		self.vehicleList.append(vehicle)
		
	def removeVehicle(self, vehicle):
		self.vehicleByColor[vehicle.color] = None
		vehicleList.remove(vehicle)