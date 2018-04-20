import sys
import threading

sys.path.insert(0, './UIWindows')
from ConfigUI import ConfigUI
from AddNewCarUI import AddNewCarUI
from EditCarUI import EditCarUI
from CarStatsUI import CarStatsUI
import threading

class UIManager(): #{
	##-----------------------------------------------------------------------------
	## Constructor
	##-----------------------------------------------------------------------------
	def __init__(self, parent, UIQueue): #{
		self.parent = parent
		self.configWindow = ConfigUI(self)
		self.addNewCarUI = AddNewCarUI(self)
		self.editCarUI = EditCarUI(self)
		self.carStatsUI = CarStatsUI(self)
		self.UIQueue = UIQueue
	#}

	##-----------------------------------------------------------------------------
	## Opens the Car Configuration Menu Window
	##-----------------------------------------------------------------------------
	def openConfigurationWindow(self): #{
		thread.start_new_thread(self.configWindow.createWindow)
		#self.configWindow.createWindow()
	#}

	##-----------------------------------------------------------------------------
	## Opens the Car Configuration Menu Window
	##-----------------------------------------------------------------------------
	def openAddNewCarUI(self): #{
		self.addNewCarUI.createWindow()
	#}

	##-----------------------------------------------------------------------------
	## Opens the Edit Car Window
	##-----------------------------------------------------------------------------
	def openEditCarUI(self, car): #{
		self.editCarUI.createWindow(car)
	#}

	##-----------------------------------------------------------------------------
	## Opens the Car Statistics Window
	##-----------------------------------------------------------------------------
	def openCarStatsUI(self): #{
		self.carStatsUI.createWindow()

		#TODO: Create a thread to constantly retrieve the car list and update the car stats frame
		#tUpdateLeaderBoard = threading.Thread(target=self.parent.leaderBoardQueue.workerLeaderBoard)
		#tUpdateLeaderBoard.start()
	#}

	##-----------------------------------------------------------------------------
	## Updates the Camera Feed
	##-----------------------------------------------------------------------------
	def updateCameraFrame(self, feed): #{
		self.carStatsUI.updateCameraFeedFrame(feed)
	#}

	##-----------------------------------------------------------------------------
	## Sends the information from addnewcar to add a new car frame in the config UI
	##-----------------------------------------------------------------------------
	def addNewCarFrame(self, carName, IP, port, controlSystem, guidanceSystem): #{
		self.carStatsUI.addNewCarCallback(carName, IP, port, controlSystem, guidanceSystem)
		
	#}

	##-----------------------------------------------------------------------------
	## Sends the information from editCar to update a car frame in the config UI
	##-----------------------------------------------------------------------------
	def deleteCarFrame(self, car): #{
		self.carStatsUI.deleteCarCallback(car)
	#}

	##-----------------------------------------------------------------------------
	## Sends the information from editCar to update a car frame in the config UI
	##-----------------------------------------------------------------------------
	def updateCarFrame(self, car): #{
		self.carStatsUI.editCarCallback(car)
	#}

	##-----------------------------------------------------------------------------
	## Updates the carFrame border color based on connection status
	##-----------------------------------------------------------------------------
	def changeCarFrameColor(self, carName, status): #{
		self.carStatsUI.updateCarFrameColor(carName, status)
	#}

	##-----------------------------------------------------------------------------
	## Adds a new car to the list of car objects
	##-----------------------------------------------------------------------------
	def addNewCarObj(self, car): #{
		self.parent.vehicles.addVehicle(car)
		#self.parent.connectNewCar(car)
	#}

	##-----------------------------------------------------------------------------
	## Returns the list of Cars
	##-----------------------------------------------------------------------------
	def getCarList(self): #{
		return self.parent.vehicles.getList()
	#}

	##-----------------------------------------------------------------------------
	## Updates the list of cars
	##-----------------------------------------------------------------------------
	def updateCarList(self, newList): #{
		self.parent.updateCarList(newList)
		#TODO: Update the IP and Port if necessary in the EthernetInterface connection
	#}

	##-----------------------------------------------------------------------------
	## Gets the a list of Control Systems
	##-----------------------------------------------------------------------------
	def getControlSystems(self): #{
		return self.parent.getControlSystems()
	#}

	##-----------------------------------------------------------------------------
	## Gets the a list of Guidance Systems
	##-----------------------------------------------------------------------------
	def getGuidanceSystems(self): #{
		return self.parent.getGuidanceSystems()
	#}

	def findTrackCallback(self): #{
                self.parent.cv.getTrack = True
        #}

        def startRace(self): #{
                self.parent.raceState = 'START'
        #}

        def pauseRace(self): #{
                self.parent.raceState = 'PAUSE'
        #}

        def stopRace(self): #{
                self.parent.raceState = 'STOP'
        #}
#}


























