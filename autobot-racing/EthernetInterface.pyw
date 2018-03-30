
import socket
import struct
import time
from subprocess import check_output as call

class EthernetInterface():
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
		except Exception as e:
			self.connection = None
			raise e
		
	def disconnectFromHost(self):
		self.connection.close()
		self.connection = None
		
	def isConnected(self):
		return bool(self.connection)