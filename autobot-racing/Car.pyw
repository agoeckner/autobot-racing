from Communication import PCConnection
#Car class to store car objects
class Car(): #{
    def __init__(self, carName, IP, port, carFrameID, frame, lapNum, place, lapTimes, controlSystem, guidanceSystem): #{
        self.carName = carName
        self.IP = IP
        self.port = port
        self.carFrameID = carFrameID
        self.frame = frame
        self.lapNum = lapNum
        self.place = place
        self.lapTimes = lapTimes
        self.controlSystem = controlSystem
        self.guidanceSystem = guidanceSystem
        self.interface = PCConnection(carName, IP, port)
    #}
#}
