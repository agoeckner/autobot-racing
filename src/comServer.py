#!/usr/bin/python           # This is server.py file

import socket
import time

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '192.168.2.4'
port = 5000

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((ip, port))
serverSocket.listen(1)

print('Server started! IP="%s" PORT="%s"' %(ip, port))
print('Waiting for connection...')

clientSocket, addr = serverSocket.accept()
print('Connection established to: ', addr)


while True:
        #add car event loop here
		#for now print what is received
		
		msg = clientSocket.recv(1024)
		print(msg.decode('ascii'))
		clientSocket.send("Ack".encode("ascii"))
		time.sleep(2);
