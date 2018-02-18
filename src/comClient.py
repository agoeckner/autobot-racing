#!/usr/bin/python3

import socket

class Car:

	name = None
	ip = None
	port = None
	connection = None
	isConnected = False

	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = port
		
	#gets attributes in tuple form (name, ip, port)
	def getAttr(self, ):
		return (name, ip, port)

	#set attributes in tuple form (name, ip, port). 
	#None can be set for any attribute to skip assignment
	def setAttr(self, attr):
		#Todo add handling if already connected!
		if attr[0]: name = attr[0]
		if attr[1]: ip = attr[1]
		if attr[2]: port = attr[2]
	
	#Simply send strings. This will change when we decide on needs to be sent.
	def sendMsg(self, str):
		connection.sendall(str.encode('ascii'))
	
	def getMsg(self):
		return connection.recv(1024).decode('ascii')
	
	def connectToHost(self):
			
		try:
			#connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			#Will raise a socket.timeout exception after 5 seconds if connection is not made
			connection = socket.create_connection((self.ip, self.port), 5)
			
		except socket.timeout:
			raise TimeoutError
		
		isConnected = True

		
	def disconnectFromHost(self):
		connection.close()
		connection = None
		isConnected = False