from math import *
import numpy as np
from numpy.linalg import *
from Utilities import *
import time

class ControlSystem:
	def __init__(self):
		pass

	# Given an actual and a desired heading, returns new delta heading value.
	def heading(self, actual, desired):
		if desired - actual > pi:
			actual += 2 * pi
		elif desired - actual < -pi:
			actual -= 2 * pi;
		return desired - actual
	
	# Given an actual and a desired throttle, returns new delta speed value.
	def throttle(self, actual, desired):
		return desired - actual

class PIControlSystem(ControlSystem):
	def __init__(self, P=1.0, I=0.5):
		self.Kp = P
		self.Ki = I
		
		self.sample_time = 0.02
		self.current_time = time.time()
		self.last_time = self.current_time
		self.clear()
		
	# Given an actual and a desired heading, returns new delta heading value.
	def heading(self, actual, desired):
		if desired - actual > pi:
			actual += 2 * pi
		elif desired - actual < -pi:
			actual -= 2 * pi;
			
		self.PID(desired, actual)
		return self.output
	
	def PID(self, SP, PV):
	
		error = SP - PV

		self.current_time = time.time()
		delta_time = self.current_time - self.last_time
		
		if (delta_time >= self.sample_time):
			self.PTerm = self.Kp * error
			self.ITerm += error * delta_time
			
			print(self.ITerm)
			if (self.ITerm < -self.windup_guard):
				print("first")
				self.ITerm = -self.windup_guard
			elif (self.ITerm > self.windup_guard):
				print("second")
				self.ITerm = self.windup_guard

			# Remember last time for next calculation
			self.last_time = self.current_time

			self.output = self.PTerm + (self.Ki * self.ITerm)
			
	#Clears PID computations and coefficients	
	def clear(self):
		self.PTerm = 0.0
		self.ITerm = 0.0
		self.output = 0.0
		self.windup_guard = 0.05

	#Determines how aggressively the PID reacts to the current error with setting Proportional Gain
	def setKp(self, proportional_gain):
		self.Kp = proportional_gain
		
	#Determines how aggressively the PID reacts to the current error with setting Integral Gain
	def setKi(self, integral_gain):
		self.Ki = integral_gain
		
	#PID that should be updated at a regular interval.
	def setSampleTime(self, sample_time):
		self.sample_time = sample_time
		
	# Given an actual and a desired throttle, returns new delta speed value.
	def throttle(self, actual, desired):
		return desired - actual
		
class GuidanceSystem:
	def __init__(self, environment):
		self.environment = environment
		self.vehicle = None #will be set by VehicleManager
		self.track = environment.track
	
	# Returns the desired heading at a specific position on the track.
	def getDesiredHeading(self, pos):
		((wall0, wall1), d) = self._getClosestPolyVertex(pos, self.track.innerWall)
		heading = atan2(wall1[1] - wall0[1], wall1[0] - wall0[0])
		return heading
	
	# Returns the desired speed at a specific position on the track.
	# Returns None if speed control is disabled.
	def getDesiredSpeed(self, pos):
		return self.vehicle.initialSpeed
	
	# Determines if a point is within the boundaries of the track.
	def isPointOnTrack(self, point):
		if isPointInPolygon(self.track.innerWall, point):
			return False
		if isPointInPolygon(self.track.outerWall, point):
			return True
		return False
	
	# Returns tuple of ((line0, line1), dist), where line0 and line1 are
	# points on closest vertex, and dist is distance to closest point on line.
	def _getClosestPolyVertex(self, pos, polygon):
		closest = ()
		min = 99999999
		p1 = polygon[0]
		for p in range(1, len(polygon)):
			p2 = polygon[p]
			d = np.cross(np.subtract(p2, p1), np.subtract(p1, pos)) / norm(np.subtract(p2, p1))
			if d < min:
				min = d
				closest = (p1, p2)
			p1 = p2
		return (closest, abs(min))

class WallFollowingGuidanceSystem(GuidanceSystem):	
	def __init__(self, *args, wallDistance = 20, lookahead = 45, **kwargs):
		super(WallFollowingGuidanceSystem, self).__init__(*args, **kwargs)
		self.desiredWallDist = wallDistance
		self.actualWallDist = 0
		self.distLookahead = lookahead

	
	# Returns the desired heading at a specific position on the track.
	def getDesiredHeading(self, pos):
		((wall0, wall1), d) = self._getClosestPolyVertex(pos, self.track.innerWall)
		self.actualWallDist = d
		# Straight-line heading along wall.
		ha = atan2(wall1[1] - wall0[1], wall1[0] - wall0[0])
		# Heading that converges to correct distance from wall.
		hd = atan2(d - self.desiredWallDist, self.distLookahead)
		heading = ha - hd
		return heading