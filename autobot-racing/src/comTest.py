
import comClient
import time
import random

myCar1 = comClient.Car("Car1", "192.168.2.4", 4000)
myCar2 = comClient.Car("Car2", "192.168.2.3", 4000)

myCar1.connectToHost();
myCar2.connectToHost();

count = 0
while True:
	if myCar1.isConnected(): myCar1.sendMsg(random.randint(-1,1), random.uniform(-1, 1))
	if myCar2.isConnected(): myCar2.sendMsg(random.randint(-1,1), random.uniform(-1, 1))
	# count += 1
	# if count == 5:
		# myCar2.disconnectFromHost()
		# time.sleep(5)
		# myCar2.connectToHost()
	# time.sleep(1)