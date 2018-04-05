import RPi.GPIO as GPIO
import spidev
import time

POT_INIT = 100
POT_TOL = 5
spi = None

#IO must be initialized BEFORE RC controller is turned on
def init():
	global spi

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup([36, 38,40], GPIO.OUT, initial=GPIO.LOW)
	
	setDirection.curr = 0;
	
	spi = spidev.SpiDev()
	spi.open(0, 0)
	spi.max_speed_hz = 244000 
	write_pot(POT_INIT)
	
def deinit():
	global spi
	
	GPIO.cleanup()
	spi.close()
	spi = None
	
	
def setPower(status):
	if(status):
		GPIO.output(36, GPIO.HIGH)
	else:
		GPIO.output(36, GPIO.LOW)
	
def setDirection(direction):
	if setDirection.curr != direction:
	
		setDirection.curr = direction
		GPIO.output([38,40], GPIO.LOW)
		
		if setDirection.curr == -1:
			GPIO.output(40, GPIO.HIGH)
		elif setDirection.curr == 1:
			GPIO.output(38, GPIO.HIGH)
		
# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb, lsb])
	
def setSpeed(speed):

	value = None

	if speed > 0:
		value = (speed - 1) + POT_INIT + POT_TOL
	elif speed < 0:
		value = (speed + 1) + POT_INIT - POT_TOL
	else:
		value = POT_INIT
		
	write_pot(value)


	
