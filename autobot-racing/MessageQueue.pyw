import thread

class MessageQueue(): #{
    ##-----------------------------------------------------------------------------
    ## Constructor
    ##-----------------------------------------------------------------------------
    def __init__(self): #{
        self.q = Queue()
    #}

    def worker(self): #{
        while True:
            message = self.q.get()
            #updateInformation(message)
    #}
#}
