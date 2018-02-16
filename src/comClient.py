#!/usr/bin/python3

import socket

class Car:

	name = None
	ip = None
	port = None
	isConnected = False

	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = port
		
	#gets attributes in tuple form (name, ip, port)
	def getAttr()
		return (name, ip, port)

	#set attributes in tuple form (name, ip, port). 
	#None can be set for any attribute to skip attr assignment
	def setAttr(attr):
		#Todo add handling if already connected!
		if attr[0]: name = attr[0]
		if attr[1]: ip = attr[1]
		if attr[2]: port = attr[2]
		
	def connectToHost():
			
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		printf('Connecting to %s..." % ip)
		s.connect((ip, port))
		printf('Connected!")

		isConnected = True
		
	def disconnectFromHost():
		s.close()
		isConnected = False