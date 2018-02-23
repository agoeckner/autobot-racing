from ConfigUI import ConfigUI
from AddNewCarUI import AddNewCarUI
from EditCarUI import EditCarUI
from CarStatsUI import CarStatsUI

class UIManager(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.parent = parent
        self.configWindow = ConfigUI(self)
        self.addNewCarUI = AddNewCarUI(self)
        self.editCarUI = EditCarUI(self)
        self.carStatsUI = CarStatsUI(self)
    #}

    ##-----------------------------------------------------------------------------
    ## Opens the Car Configuration Menu Window
    ##-----------------------------------------------------------------------------
    def openConfigurationWindow(self): #{
        self.configWindow.createWindow()
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
    def openEditCarUI(self, carName, IP, port, frame): #{
        self.editCarUI.createWindow(carName, IP, port, frame)
    #}

    ##-----------------------------------------------------------------------------
    ## Opens the Car Statistics Window
    ##-----------------------------------------------------------------------------
    def openCarStatsUI(self): #{
        self.carStatsUI.createWindow()
    #}

    ##-----------------------------------------------------------------------------
    ## Sends the information from addnewcar to add a new car frame in the config UI
    ##-----------------------------------------------------------------------------
    def addNewCarFrame(self, carName, IP, port): #{
        self.carStatsUI.addNewCarCallback(carName, IP, port)
    #}

    ##-----------------------------------------------------------------------------
    ## Sends the information from editCar to update a car frame in the config UI
    ##-----------------------------------------------------------------------------
    def deleteCarFrame(self, frame): #{
        self.carStatsUI.deleteCarCallback(frame)
    #}

    ##-----------------------------------------------------------------------------
    ## Sends the information from editCar to update a car frame in the config UI
    ##-----------------------------------------------------------------------------
    def updateCarFrame(self, carName, IP, port, frame): #{
        self.carStatsUI.editCarCallback(carName, IP, port, frame)
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
        self.parent.carList.append(car)
        print(str(self.parent.carList))
    #}

    ##-----------------------------------------------------------------------------
    ## Returns the list of Cars
    ##-----------------------------------------------------------------------------
    def getCarList(self): #{
        return self.parent.getCarList()
    #}

    ##-----------------------------------------------------------------------------
    ## Updates the list of cars
    ##-----------------------------------------------------------------------------
    def updateCarList(self, newList): #{
        self.parent.updateCarList(newList)
    #}
#}


























