from collections import deque
from EthernetInterface import EthernetInterface
from pykalman import KalmanFilter
import numpy as np
import sys
import time

# TEMPORARY...
from matplotlib import pyplot as plt

import controls as ngc

#Car class to store car objects
class Vehicle():
	POSITION_HISTORY_POINTS = 10
	HEADING_HISTORY_POINTS = 10
	
	# The maximum amount of time that a vehicle may be "missing" before stop command is sent.
	EMERGENCY_STOP_TIMEOUT = 2 #seconds

	def __init__(self, parent, name, IP, port, carFrameID, frame, controlSystem,
		guidanceSystem,
		initialSpeed = 0.1):
		
		# Set up parameters.
		self.parent = parent
		self.name = name
		self.color = (0, 0, 0)
		self.IP = IP
		self.port = port
		self.carFrameID = carFrameID
		self.frame = frame
		self.initialSpeed = initialSpeed
		
		# The position filter has not yet been initialized.
		self.filterInitialized = False
		self.posFilter = None
		
		# Get the actual control system class.
		# print("Got control system: " + str(controlSystem))
		self.control = parent.parent.controlSystems[controlSystem]()
		print("Vehicle " + str(name) + " using control system: " + str(self.control))
		self.guidance = parent.parent.guidanceSystems[guidanceSystem](self.parent.parent,
			wallDistance = 20, lookahead = 100)
		print("Vehicle " + str(name) + " using guidance system: " + str(self.guidance))
		self.guidance.vehicle = self
		
		# self.control = ngc.ControlSystem()
		# self.guidance = ngc.WallFollowingGuidanceSystem(self.parent.parent,
			# wallDistance = 20, lookahead = 100)
		
		self.interface = EthernetInterface(name, IP, port)
		
		# Get colors... This is ugly.
		if name.upper() == "RED":
			self.color = (255, 0, 0)
		elif name.upper() == "GREEN":
			self.color = (0, 255, 0)
		elif name.upper() == "BLUE":
			self.color = (0, 0, 255)
		
		# Store the most recent position/heading data.
		self.position = deque(maxlen = self.POSITION_HISTORY_POINTS)
		self.heading = deque(maxlen = self.HEADING_HISTORY_POINTS)
		
		# These variables store the desired heading/speed.
		# AKA, the output of the guidance system.
		self.desiredHeading = 0.0
		self.desiredSpeed = 0
		
		# These variables store the current, filtered telemetry data.
		# AKA, the output of the Kalman Filter.
		self.actualHeading = 0.0
		self.actualPosition = (0.0, 0.0)
		self.actualSpeed = 0
		
		# Add dummy initial data.
		self.lastTelemetryTime = time.time()
		self.position.append((0,0))
		self.heading.append(0)
		
		# Connect to Pi.
		if self.connect():
			print("Vehicle \"" + str(self.name) + "\" connected to transmitter.")
		else:
			print("WARN: Vehicle \"" + str(self.name) + "\" failed to connect to transmitter!")
	
	def getCurrentStateVector(self):
		# state vector is [X, dX/dt, Y, dY/dt]
		#TODO
		return [self.position[0], self.velocity[0], self.position[0][1], self.velocity[1]]
	
	def initializePositionFilter(self):
	
		# Decent explanation of Kalman parameters here:
		# https://stackoverflow.com/questions/47210512/using-pykalman-on-raw-acceleration-data-to-calculate-position
	
		# Time step
		dt = 0.01 #TODO, update on actual delta time
		
		# Transition matrix (system dynamics)
		transitionMatrix = [[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]]
		
		# Observation matrix
		observationMatrix = [1,0,0]
		
		# Get the initial state.
		#TODO
		initState = self.getCurrentStateVector()
		
		# Covariances
		initialStateCov = 1.0e-3 * np.eye(4)
		transistionCov = 1.0e-4 * np.eye(4)
		observationCov = 1.0e-1 * np.eye(2)
		
		# Set up the filter.
		self.posFilter = KalmanFilter(
			transition_matrices = transitionMatrix,
			observation_matrices = observationMatrix,
			initial_state_mean = initState,
            initial_state_covariance = initialStateCov,
            transition_covariance = transistionCov,
            observation_covariance = observationCov)
		
		print("Filter initialized: " + str(self.posFilter))
		
		self.filterInitialized = True
	
	def updateTelemetry(self, position, heading):
	
		# Initialize the position filter once we have enough data.
		if not self.filterInitialized and len(self.position) > 2:
			self.initializePositionFilter()
		
		# Add to the telemetry history.
		self.position.append(position)
		self.heading.append(heading)
		
		# Get the latest time.
		currentTime = time.time()
		deltaTime = currentTime - self.lastTelemetryTime
		
		# Calculate vehicle speed/velocity.
		self.velocity = tuple(np.divide(np.array(self.position[1]) - \
			np.array(position), deltaTime))
		# print("VELOCITY: " + str(self.velocity))
		
		# TODO: JUST CALCULATE THIS FROM VELOCITY
		deltaPos = abs(np.linalg.norm(np.array(self.position[1]) - \
			np.array(position)))
		self.actualSpeed = deltaPos / deltaTime
		# print("SPEED: " + str(self.actualSpeed))
		
		# Update last telemetry time.
		self.lastTelemetryTime = currentTime
		
		# Do Kalman things.
		if self.filterInitialized and len(self.position) == 10:
			data = list(self.position)
			print("MEASURED:")
			print(data)
			(filtered_state_means, filtered_state_covariances) = self.posFilter.filter(data)
			print("FILTERED:")
			print(filtered_state_means)
			exit(0)
			# plt.plot(data[:,0],data[:,1],'xr',label='measured')
			# plt.axis([0,520,360,0])
				# plt.hold(True)
			# plt.plot(filtered_state_means[:,0],filtered_state_means[:,1],'ob',label='kalman output')
			# plt.legend(loc=2)
			# plt.title("Constant Velocity Kalman Filter")
			# plt.show()
			
	
	def runNavGuidanceControl(self):
		# Automatically stop if we have no received telemetry recently.
		ltt = self.lastTelemetryTime
		if ltt != None and (time.time() - ltt) >= self.EMERGENCY_STOP_TIMEOUT:
			self.sendMsg(0, 0.0)
			print("WARN: Vehicle " + str(self.name) + " has been stopped.")
			return
		
		# Determine guidance.
		desiredHeading = self.guidance.getDesiredHeading(self.actualPosition)
		desiredSpeed = self.guidance.getDesiredSpeed(self.actualPosition)
		
		# Run control algorithm.
		deltaHeading = self.control.heading(self.actualHeading, desiredHeading)
		deltaSpeed = self.control.throttle(self.actualSpeed, desiredSpeed)
		
		# Update the desired speed/heading values.
		self.updateHeading(deltaHeading)
		self.updateSpeed(deltaSpeed)
		
		# Snap steering  to trinary, the only steering available on these cars.
		hdg = self.desiredHeading
		if hdg < 0.0:
			# print("TURN LEFT?")
			hdg = -1
		elif hdg > 0.0:
			# print("TURN RIGHT?")
			hdg = 1
		else:
			hdg = 0
			
		# TEMPORARY INVERSE
		# hdg = -hdg
		
		# Send command to the car.
		self.sendMsg(hdg, self.desiredSpeed)
	
	def updateHeading(self, deltaHeading):
		self.desiredHeading += deltaHeading
	
	def updateSpeed(self, deltaSpeed):
		self.desiredSpeed += deltaSpeed
	
	#
	# Communication functions:
	#
	
	def connect(self):
		try:
			self.interface.connectToHost()
			return True
		except (ConnectionError, OSError) as e:
			return False
			
	def disconnect(self):
		self.interface.disconnectFromHost()
		
	def sendMsg(self, direction, speed):
		try:
			self.interface.sendMsg(direction, speed)
			return True
		except (ConnectionError, OSError) as e:
			return False
