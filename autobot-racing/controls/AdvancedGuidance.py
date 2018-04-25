from math import *
# import numpy as np
# from numpy.linalg import *
from Utilities import *
from .Controls import *

class PassingGuidanceSystem(WallFollowingGuidanceSystem):
	FOLLOW_PASS_THRESHOLD_DIST = 60
	MIN_PASS_SPACING = 15
	CAUTION_DISTANCE = 10
	CAUTION_SPEED_PERCENTAGE = 0.5
	
	def __init__(self, *args, **kwargs):
		super(PassingGuidanceSystem, self).__init__(*args, **kwargs)
		self.origWallDist = self.desiredWallDist
	
	def getDesiredSpeed(self, pos):
		vehicle = self.vehicle

		# Check for collisions with the walls.
		((wall0, wall1), d) = self._getClosestPolyEdge(pos, self.environment.track.innerWall)
		if d < self.CAUTION_DISTANCE:
			# print("TOO CLOSE TO INNER WALL")
			return vehicle.initialSpeed * self.CAUTION_SPEED_PERCENTAGE
		((wall0, wall1), d) = self._getClosestPolyEdge(pos, self.environment.track.outerWall)
		if d < self.CAUTION_DISTANCE:
			# print("TOO CLOSE TO OUTER WALL")
			return vehicle.initialSpeed * self.CAUTION_SPEED_PERCENTAGE
		
		# Check for collisions with other vehicles.
		vehicles = self.environment.vehicles
		for v in vehicles:
			if v == vehicle:
				continue
			if vehicle.actualSpeed < v.actualSpeed or v.actualSpeed == 0:
				continue
			d = euclideanDistance(pos, v.position)
			if d < 5:
				raise Exception("COLLISION")
			if d < self.CAUTION_DISTANCE:
				# print("TOO CLOSE TO OTHER VEHICLE")
				return (vehicle.actualSpeed + v.actualSpeed) * self.CAUTION_SPEED_PERCENTAGE
		return self.vehicle.initialSpeed
	
	# Returns the desired heading at a specific position on the track.
	def getDesiredHeading(self, pos):
		# Attempt to pass if necessary.
		self.desiredWallDist = self.getPassingWallDist(self.vehicle)
		
		# Now use the wall-following algorithm.
		return super(PassingGuidanceSystem, self).getDesiredHeading(pos)
	
	# Determines how much the wall distance needs to change in order to pass.
	def getPassingWallDist(self, vehicle):
		vehicles = self.environment.vehicles
		for v in vehicles:
			if v == vehicle:
				continue
			d = euclideanDistance(vehicle.position, v.position)
			if d > self.FOLLOW_PASS_THRESHOLD_DIST:
				continue
			if v.actualSpeed >= vehicle.actualSpeed:
				continue
			# print("PASSING")
			# if abs(v.guidance.actualWallDist - self.desiredWallDist) >= self.MIN_PASS_SPACING:
				# return self.desiredWallDist
			spacing = abs(v.guidance.actualWallDist - self.actualWallDist)
			if spacing >= self.MIN_PASS_SPACING:
				return self.desiredWallDist
				
			# Do we pass on the inside or the outside?
			adjust = max(self.MIN_PASS_SPACING, spacing)
			if v.guidance.actualWallDist > 2 * self.MIN_PASS_SPACING:
				adjust *= -1
			return v.guidance.actualWallDist + adjust
		# print("NOT PASSING")
		return self.origWallDist