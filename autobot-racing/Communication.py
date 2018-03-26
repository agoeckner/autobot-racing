#!/usr/bin/python3

import socket
import struct
import time
from subprocess import check_output as call
import driver


class PCConnection:

	name = None
	ip = None
	port = None
	connection = None
	packer = None

	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = port
		self.packer = struct.Struct('=h h')
		
	#gets attributes in tuple form (name, ip, port)
	def getAttr(self):
		return (self.name, self.ip, sefl.port)

	#set attributes in tuple form (name, ip, port). 
	#None can be set for any attribute to skip assignment
	def setAttr(self, attr):
		if attr[0]: self.name = attr[0]
		if attr[1]: self.ip = attr[1]
		if attr[2]: self.port = attr[2]
	
	#We will send 4 bytes (2 byte short steering, 2 byte short speed)
	#Steering is designated as: -1 Left; 0 Straight; 1 Right
	#Speed is designated as <0 Reverse; 0 Off; >1 Forward
	def sendMsg(self, steering, speed):
		try:
			
			bin = self.packer.pack(steering, speed)
			self.connection.sendall(bin)
			
		except Exception:
			self.connection = None
			raise
	
	def getMsg(self):
		try:
			return self.connection.recv(1024).decode('ascii')
		except Exception:
			self.connection = None
			raise
	
	def connectToHost(self):
		#Will raise a socket.timeout exception after 5 seconds if connection is not made
		try:
			self.connection = socket.create_connection((self.ip, self.port), 5)
		except Exception:
			self.connection = None
		
	def disconnectFromHost(self):
		self.connection.close()
		self.connection = None
		
	def isConnected(self):
		return bool(self.connection)
		

class PiConnection:

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
	def evt_loop(self):


                try:
                        driver.init()
                        print("Starting Event Loop")
                        
                        while True:
                                data = self.getMsg()
                                driver.setDirection(data[0])
                                driver.setSpeed(data[1])

                        
                except Exception:
                        pass
                
                finally:
                        driver.deinit()

                
