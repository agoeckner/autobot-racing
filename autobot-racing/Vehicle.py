from collections import deque
from EthernetInterface import EthernetInterface
from pykalman import KalmanFilter
import numpy as np
import sys
import time
import math
import random

# TEMPORARY...
from matplotlib import pyplot as plt

import controls as ngc

#Car class to store car objects
class Vehicle():
	POSITION_HISTORY_POINTS = 10
	HEADING_HISTORY_POINTS = 10
	
	# The maximum amount of time that a vehicle may be "missing" before stop command is sent.
	EMERGENCY_STOP_TIMEOUT = 0.50 #seconds

	def __init__(self, parent, name, IP, port, carFrameID, frame, statFrame, controlSystem,
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
		self.statFrame = statFrame
		self.initialSpeed = initialSpeed
		self.lastLapTime = 0.00
		self.inStartPoly = False
		self.place = 0
		self.lapNum = 0
		
		# The position filter has not yet been initialized.
		self.filterInitialized = False
		self.posFilter = None
		
		# Get the actual control system class.
		# print("Got control system: " + str(controlSystem))
		self.control = parent.parent.controlSystems[controlSystem]()
		print("Vehicle " + str(name) + " using control system: " + str(self.control))
		self.guidance = parent.parent.guidanceSystems[guidanceSystem](self.parent.parent,
			wallDistance = 15, lookahead = 200)
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
		elif name.upper() == "YELLOW":
			self.color = (255,255,0)
		
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
		# state vector is [X, Y, dX/dt, dY/dt]
		#TODO
		pos = self.position[0]
		vel = self.velocity
		return [pos[0], vel[0], pos[1], vel[1]]
	
	def initializePositionFilter(self):
	
		# Decent explanation of Kalman parameters here:
		# https://stackoverflow.com/questions/47210512/using-pykalman-on-raw-acceleration-data-to-calculate-position
		# https://pykalman.github.io/#pykalman.KalmanFilter.filter_update
	
		# Time step
		dt = 0.01 #TODO, update on actual delta time
		
		# Transition matrix (system dynamics, F)
		transitionMatrix = [[1,dt,0,0],[0,1,0,0],[0,0,1,dt],[0,0,0,1]]
		
		# Observation matrix, H
		observationMatrix = [[1,0,0,0], [0,0,1,0]]
		
		# Get the initial state.
		#TODO
		initState = self.getCurrentStateVector()
		
		# Covariances
		initialStateCov = 1.0e-2 * np.eye(4)
		transistionCov = 1.0e-4 * np.eye(4)
		observationCov = 1.0e-4 * np.eye(2)
		
		# Set up k-1 state
		self.prevStateVector = initState
		self.prevStateCovariance = initialStateCov
		
		# Set up the filter.
		self.posFilter = KalmanFilter(
			transition_matrices = transitionMatrix,
			observation_matrices = observationMatrix,
			initial_state_mean = initState,
            initial_state_covariance = initialStateCov,
            transition_covariance = transistionCov,
            observation_covariance = observationCov)
		
		print("Filter initialized: " + str(self.posFilter))
		print("Used initial state: " + str(initState))
		print(self.position)
		
		self.filterInitialized = True
	
	# This must occur before position/velocity is updated.
	def updatePositionFilter(self, position, deltaTime):
		filtered_state_mean = self.prevStateVector
		filtered_state_covariance = self.prevStateCovariance
		observation = list(position)
		transitionMatrix = [[1,deltaTime,0,0],[0,1,0,0],[0,0,1,deltaTime],[0,0,0,1]]
		
		# Update the filter.
		(next_filtered_state_mean, next_filtered_state_covariance) = self.posFilter.filter_update(
			filtered_state_mean, filtered_state_covariance, observation = observation,
			)#transition_matrix = transitionMatrix)
		
		self.prevStateVector = next_filtered_state_mean
		self.prevStateCovariance = self.prevStateCovariance
		
		filteredPos = (next_filtered_state_mean[0], next_filtered_state_mean[2])
		
		# print("RAW POSITION: " + str(position))
		# print("FILTERED POSITION: " + str(filteredPos))
		
		return filteredPos
	
	def updateTelemetry(self, rawPosition, heading):
	
		# Initialize the position filter once we have enough data.
		if not self.filterInitialized and len(self.position) > 2:
			self.initializePositionFilter()
		
		# Get the latest time.
		currentTime = time.time()
		deltaTime = currentTime - self.lastTelemetryTime
		if deltaTime == 0.0:
			deltaTime = 0.0000001
		
		# Do Kalman things.
		if self.filterInitialized:
			position = self.updatePositionFilter(rawPosition, deltaTime)
			# print("Got new filtered position: " + str(position))
		else:
			position = rawPosition
			# print("Got raw position: " + str(position))
		
		# Add to the telemetry history.
		self.actualPosition = position
		self.actualHeading = heading
		self.position.appendleft(position)
		self.heading.appendleft(heading)
		
		# Calculate vehicle speed/velocity.
		self.velocity = tuple(np.divide(np.array(self.position[1]) - \
			np.array(position), deltaTime))
		self.actualSpeed = np.sqrt(np.dot(self.velocity, self.velocity))
		
		# Update last telemetry time.
		self.lastTelemetryTime = currentTime
		
	
	def runNavGuidanceControl(self):
		if self.parent.parent.raceState is 'STOP' or self.parent.parent.raceState is 'PAUSE':
			self.sendMsg(0, 0.0)
			return
		
		# Automatically stop if we have no received telemetry recently.
		ltt = self.lastTelemetryTime
		if ltt != None and (time.time() - ltt) >= self.EMERGENCY_STOP_TIMEOUT:
			self.sendMsg(0, 0.0)
			print("WARN: Vehicle " + str(self.name) + " has been stopped. [TIMEOUT]")
			return
		
		# Automatically stop if we go outside the track.
		# if not self.guidance.isPointOnTrack(self.actualPosition):
			# self.sendMsg(0, 0.0)
			# print("WARN: Vehicle " + str(self.name) + " has been stopped. [OUT OF BOUNDS]")
			# return
		
		# Determine guidance.
		desiredHeading = self.guidance.getDesiredHeading(self.actualPosition)
		desiredSpeed = self.guidance.getDesiredSpeed(self.actualPosition)
		
		# Clamp headings between 0 and 2 * PI.
		self.actualHeading = self.actualHeading % (2 * math.pi)
		desiredHeading = desiredHeading % (2 * math.pi)
		
		# Run control algorithm.
		deltaHeading = self.control.heading(self.actualHeading, desiredHeading)
		deltaSpeed = self.control.throttle(self.actualSpeed, desiredSpeed)
		
		# print("DESIRED HEADING: " + str(math.degrees(desiredHeading)))
		# print("ACTUAL HEADING: " + str(math.degrees(self.actualHeading)))
		# print("DELTA HEADING: " + str(str(math.degrees(deltaHeading))))
		
		# Update the desired speed/heading values.
		self.updateDesiredHeading(desiredHeading)
		self.updateDesiredSpeed(desiredSpeed)
		# if self.name == "BLUE":
			# self.desiredSpeed = 0.1
		# else:
			# self.desiredSpeed = 0.2
		# if random.randint(0,1) == 0:
			# self.desiredSpeed = 0.1
		# else:
		# self.desiredSpeed = 0.2
		# print(self.desiredSpeed)
		
		# Snap steering  to trinary, the only steering available on these cars.
		if abs(deltaHeading) < math.radians(5):
			hdg = 0.0
		else:
			hdg = deltaHeading
		
		if hdg < 0.0:
			hdg = -1
		elif hdg > 0.0:
			hdg = 1
		else:
			hdg = 0
		
		# Send command to the car.
		self.sendMsg(hdg, self.desiredSpeed)
	
	def updateDesiredHeading(self, desiredHeading):
		self.desiredHeading = desiredHeading
		# self.desiredHeading = desiredHeading % 2 * math.pi #(2 * math.pi)
		# if abs(deltaHeading) >= 5.0:
			# self.desiredHeading += deltaHeading
			# self.desiredHeading = self.desiredHeading % 2 * math.pi #(2 * math.pi)
	
	def updateDesiredSpeed(self, desiredSpeed):
		self.desiredSpeed = desiredSpeed
		# print("DESIRED SPEED: " + str(self.desiredSpeed) + " (update: " + str(deltaSpeed) + ")")
	
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
