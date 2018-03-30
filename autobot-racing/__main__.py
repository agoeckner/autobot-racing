from EthernetInterface import EthernetInterface
from UIManager import UIManager
from cv.ComputerVision import *
import threading
from MessageQueue import MessageQueue

class FrameworkManager(): #{
        ##-----------------------------------------------------------------------------
        ## Constructor
        ##-----------------------------------------------------------------------------
        def __init__(self): #{
                self.cv = ComputerVision(self)
                self.UserInterface = UIManager(self)
                self.EthernetInterface = EthernetInterface(self)
                self.carList = [] #Stores all car objects
                self.UIQueue = MessageQueue(self)
        #}

        ##-----------------------------------------------------------------------------
        ## Starts the program
        ##-----------------------------------------------------------------------------
        def startup(self): #{
                tUI = threading.Thread(target=self.UserInterface.openCarStatsUI)
                tCV = threading.Thread(target=self.cv.run, args=(True,))
                tCV.setDaemon(True)
                tUI.start()
                tCV.start()

                while True: #{
                        if not tUI.isAlive():
                                break
                #}
        #}

##Car Methods-----------------------------------------------------------------------------------------------------------------------------------------
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
                print(len(self.carList))
        #}
##----------------------------------------------------------------------------------------------------------------------------------------------------


##UI Methods------------------------------------------------------------------------------------------------------------------------------------------
        ##-----------------------------------------------------------------------------
        ## Updates the list of cars
        ##-----------------------------------------------------------------------------
        def updateCarFrameColor(self, carName, status): #{
                self.UserInterface.changeCarFrameColor(carName, status)
        #}

        ##-----------------------------------------------------------------------------
        ## Gets the a list of Control Systems
        ##-----------------------------------------------------------------------------
        def getControlSystems(self): #{
                return ['Option 1', 'Option 2']
        #}

        ##-----------------------------------------------------------------------------
        ## Gets the a list of Guidance Systems
        ##-----------------------------------------------------------------------------
        def getGuidanceSystems(self): #{
                return ['Option 1', 'Option 2']
        #}

##----------------------------------------------------------------------------------------------------------------------------------------------------



##EthernetInterface Functions-------------------------------------------------------------------------------------------------------------------------
        ##-----------------------------------------------------------------------------
        ## Connects to the PI of the newly added car
        ##-----------------------------------------------------------------------------
        def connectNewCar(self, car): #{
                self.EthernetInterface.connectToPI(car)
        #}

        ##-----------------------------------------------------------------------------
        ## Updates the connection of the specified car
        ##-----------------------------------------------------------------------------
        def updateCarConnection(self, car): #{
                self.EthernetInterface.updateConnection(car)
        #}

        ##-----------------------------------------------------------------------------
        ## Disconnects from the specified car
        ##-----------------------------------------------------------------------------
        def removeConnection(self, car): #{
                self.EthernetInterface.disconnectFromPI(car)
        #}
##----------------------------------------------------------------------------------------------------------------------------------------------------

#}

if __name__ == "__main__":
        manager = FrameworkManager()
        manager.startup()
