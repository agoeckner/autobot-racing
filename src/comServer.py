#!/usr/bin/python           # This is server.py file

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostbyname()
ip = socket.gethostbyname(hostname)
port = 5000

s.bind((ip, port))
s.listen()

print('Server started!')
print('Waiting for connection...')

con = s.accept()
print('Connection established to: ', con[0])

while True:
        #add car event loop here
        pass
    
