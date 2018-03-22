import RPi.GPIO as GPIO
import spidev
import time

POT_MAX = 0X26

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup([38,40], GPIO.OUT, initial=GPIO.LOW)
	setDirection.curr = 0;
	spi = spidev.SpiDev()
	spi.open(0, 0)
	spi.max_speed_hz = 244000
	
# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb, lsb])
	
def setDirection(direction):
	if setDirection.curr != direction:
	
		setDirection.curr == direction
		GPIO.output([38,40], GPIO.LOW)
		
		if setDirection.curr == -1:
			GPIO.output(38, GPIO.HIGH)
		elif setDirection.curr == 1:
			GPIO.output(40, GPIO.HIGH)
		
	
def setSpeed(speed):
	if(speed >= 0 && speed <= POT_MAX):
		write_pot(speed)
		return True
	else:
		return False