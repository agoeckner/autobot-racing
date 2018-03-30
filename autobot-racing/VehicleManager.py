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
		
		# TODO: THIS IS TEMPORARY CODE, REMOVE ONCE COLOR CAN BE SPECIFIED IN UI
		vehicle.color = self.COLORS[len(self.vehicleList)]
	
		self.vehicleByColor[vehicle.color] = vehicle
		self.vehicleList.append(vehicle)
		
	def removeVehicle(self, vehicle):
		self.vehicleByColor[vehicle.color] = None
		vehicleList.remove(vehicle)