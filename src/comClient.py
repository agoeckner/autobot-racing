#!/usr/bin/python3

import socket

class Car:

	name = None
	ip = None
	port = None

	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = port
		
	#gets attributes in tuple form (name, ip, port)
	def getAttr(self):
		return (self.name, self.ip, sefl.port)

	#set attributes in tuple form (name, ip, port). 
	#None can be set for any attribute to skip assignment
	def setAttr(self, attr):
		if attr[0]: self.name = attr[0]
		if attr[1]: self.ip = attr[1]
		if attr[2]: self.port = attr[2]
	
	#Simply send strings. This will change when we decide on needs to be sent.
	def sendMsg(self, str):
		try:
			self.connection.sendall(str.encode('ascii'))
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
		self.connection = socket.create_connection((self.ip, self.port), 5)
		
	def disconnectFromHost(self):
		self.connection.close()
		self.connection = None