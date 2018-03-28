import queue

class MessageQueue(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self, parent): #{
        self.q = queue.Queue()
        self.parent = parent
    #}

    def worker(self): #{
        while True:
            message = self.q.get()
            if message[0] == 'CamFeed':
                self.updateUI(message[1])
    #}

    def updateUI(self, feed): #{
        self.parent.UserInterface.updateCameraFrame(feed)
    #}
#}
