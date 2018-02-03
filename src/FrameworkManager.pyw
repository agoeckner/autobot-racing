from EthernetInterface import EthernetInterface
from UIManager import UIManager

class FrameworkManager(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self): #{
        self.UserInterface = UIManager(self)
        self.EthernetInterface = EthernetInterface(self)
        
    #}

    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def startup(self): #{
        self.ui.createWindow()
    #}
#}

if __name__ == "__main__":
    manager = FrameworkManager()
    manager.startup()
