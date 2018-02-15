from ConfigUI import ConfigUI

class UIManager(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self): #{
        #self.parent = parent
        self.configWindow = ConfigUI(self)
    #}

    ##-----------------------------------------------------------------------------
    ## Opens the Car Configuration Menu Window
    ##-----------------------------------------------------------------------------
    def openConfigurationWindow(self): #{
        self.configWindow.createWindow()
    #}
#}


ui = UIManager()
ui.openConfigurationWindow()
