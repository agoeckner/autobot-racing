#!/usr/bin/python           # This is server.py file

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
ip = "192.168.2.3" #socket.gethostbyname(hostname)
port = 5000

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ip, port))
s.listen()

print('Server started! IP="%s" PORT="%s"' %(ip, port))
print('Waiting for connection...')

con = s.accept()
#s.setblocking(False)
print('Connection established to: ', con[0])

while True:
        #add car event loop here
		#for now print what is received
		
		msg = s.recv(1024)
		print(msg.decode('ascii'))
		s.send("Ack".encode("ascii"))
		time.sleep(2);