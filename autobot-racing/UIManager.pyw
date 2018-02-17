from ConfigUI import ConfigUI
from AddNewCarUI import AddNewCarUI

class UIManager(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self): #{
        #self.parent = parent
        self.configWindow = ConfigUI(self)
        self.addNewCarUI = AddNewCarUI(self)
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
    ## Sends the information from addnewcar to add a new car frame in the config UI
    ##-----------------------------------------------------------------------------
    def addNewCarFrame(self, carName, IP, port): #{
        self.configWindow.addNewCarCallback(carName, IP, port)
    #}
#}


ui = UIManager()
ui.openConfigurationWindow()
