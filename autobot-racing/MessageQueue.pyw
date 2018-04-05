import queue

class MessageQueue(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.q = queue.Queue()
        self.parent = parent
    #}

    ##-----------------------------------------------------------------------------
    ## Sends the Camera Feed to the UI
    ##-----------------------------------------------------------------------------
    def workerUI(self): #{
        while True:
            #print('CAlling')
            message = self.q.get()
            self.updateUI(message[1])
            #self.parent.UserInterface.carStatsUI.updateLeaderBoard(self.parent.carList)
    #}

    
    def workerCV(self): #{
        while True:
            message = self.q.get()
            
    #}

    def updateUI(self, feed): #{
        self.parent.UserInterface.updateCameraFrame(feed)
    #}
#}
