#!/usr/bin/python3

import socket
import struct
from subprocess import check_output as call
import RCDriver

class EthernetInterface:

	ip = None
	port =  None
	addr = None
	serverSocket = None
	clientSocket = None
	unpacker = None
	
	def __init__(self):
		
		#messages should be formated (2 byte short, 4 byte float)
		self.unpacker = struct.Struct('=h f')
		
		#Grab LAN ip address. 
		#Note: we cannot use socket related functions as they return a loopback address		
		self.ip = call(['hostname', '-I'])
		self.port = 4000
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serverSocket.bind((self.ip, self.port))
		self.serverSocket.listen(0)
		

	def connectToClient(self):
		self.clientSocket, self.addr = self.serverSocket.accept()

	def disconnectFromClient(self):
		self.clientSocket.close()
		self.clientSocket = None
		
	def sendMsg(self, str):
		try:
			self.clientSocket.sendall(str.encode('ascii'))
		except Exception:
			self.clientSocket = None
			raise
	
	def getMsg(self):
		
		try:
		
			bin = self.clientSocket.recv(self.unpacker.size)
			
			if len(bin) != self.unpacker.size:
				raise ConnectionError("Unexpected bytes from pipe: expected %i, received %i" % (self.unpacker.size, len(bin)))
				
			data = self.unpacker.unpack(bin)
			return data
			
		except Exception:
			self.clientSocket = None
			raise
			
			
#Cars event loop
#All Exception handling to be done here
while True:

	try:
		RCDriver.init()
		interface = EthernetInterface()
		interface.connectToClient()
		
		print("Starting Event Loop")
		while True:
				data = interface.getMsg()
				RCDriver.setDirection(data[0])
				RCDriver.setSpeed(data[1] * 10)		#RCDriver expects an integer.
			
	except Exception:
			pass

	finally:
			RCDriver.deinit()


