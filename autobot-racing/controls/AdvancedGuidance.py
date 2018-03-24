from math import *
# import numpy as np
# from numpy.linalg import *
from Utilities import *
from .Controls import *

class PassingGuidanceSystem(WallFollowingGuidanceSystem):
	FOLLOW_PASS_THRESHOLD_DIST = 40
	MIN_PASS_SPACING = 15
	
	def __init__(self, *args, **kwargs):
		super(PassingGuidanceSystem, self).__init__(*args, **kwargs)
		self.origWallDist = self.desiredWallDist
	
	# Returns the desired heading at a specific position on the track.
	def getDesiredHeading(self, pos):
		# Get distance from wall.
		((wall0, wall1), d) = self._getClosestPolyVertex(pos, self.track.innerWall)
		self.actualWallDist = d
		
		# Attempt to pass if necessary.
		wallDist = self.getPassingWallDist(self.vehicle)
		self.desiredWallDist = wallDist
		
		# Straight-line heading along wall.
		ha = atan2(wall1[1] - wall0[1], wall1[0] - wall0[0])
		
		# Heading that converges to correct distance from wall.
		hd = atan2(d - wallDist, self.distLookahead)
		heading = ha - hd
		
		return heading
	
	# Determines how much the wall distance needs to change in order to pass.
	def getPassingWallDist(self, vehicle):
		vehicles = self.environment.vehicles
		for v in vehicles:
			if v == vehicle:
				continue
			d = euclideanDistance(vehicle.position, v.position)
			if d > self.FOLLOW_PASS_THRESHOLD_DIST:
				continue
			if v.speed >= vehicle.speed:
				continue
			# print("PASSING")
			if abs(v.guidance.actualWallDist - self.desiredWallDist) >= self.MIN_PASS_SPACING:
				return self.desiredWallDist
			return v.guidance.actualWallDist + self.MIN_PASS_SPACING
		# print("NOT PASSING")
		return self.origWallDist