from EthernetInterface import EthernetInterface
from UIManager import UIManager

class FrameworkManager(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self): #{
        self.UserInterface = UIManager(self)
        self.EthernetInterface = EthernetInterface(self)
        self.carList = []
    #}

    ##-----------------------------------------------------------------------------
    ## Opens the User Interface
    ##-----------------------------------------------------------------------------
    def startup(self): #{
        self.UserInterface.openCarStatsUI()
    #}

    ##-----------------------------------------------------------------------------
    ## Returns the current list of cars
    ##-----------------------------------------------------------------------------
    def getCarList(self): #{
        return self.carList
    #}

    ##-----------------------------------------------------------------------------
    ## Updates the list of cars
    ##-----------------------------------------------------------------------------
    def updateCarList(self, newList): #{
        self.carList = newList
    #}
#}

if __name__ == "__main__":
    manager = FrameworkManager()
    manager.startup()
