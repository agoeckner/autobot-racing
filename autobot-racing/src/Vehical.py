

import EthernetInterface

class Vehical:
	
	name = None
	position = None
	laps = None
	control = None
	navigation = None	
	interface = None

	def __init__(self, name, ip, port, control, navigation):
		self.name = name;
		self.laps = 0
		self.control = control
		self.navigation = navigation
		self.interface = EthernetInterface(name, ip, port)

		