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
            message = self.q.get()
            self.updateUI(message[1])
    #}

    
    def workerCV(self): #{
        while True:
            message = self.q.get()
            
    #}

    def updateUI(self, feed): #{
        self.parent.UserInterface.updateCameraFrame(feed)
    #}
#}
