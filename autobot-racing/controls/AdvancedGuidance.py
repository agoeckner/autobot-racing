from math import *
# import numpy as np
# from numpy.linalg import *
from Utilities import *
from .Controls import *

class PassingGuidanceSystem(WallFollowingGuidanceSystem):	
	def __init__(self, *args, **kwargs):
		super(PassingGuidanceSystem, self).__init__(*args, **kwargs)
	
	# Returns the desired heading at a specific position on the track.
	def getDesiredHeading(self, pos):
		((wall0, wall1), d) = self._getClosestPolyVertex(pos, self.track.innerWall)
		# Straight-line heading along wall.
		ha = atan2(wall1[1] - wall0[1], wall1[0] - wall0[0])
		# Heading that converges to correct distance from wall.
		hd = atan2(d - self.distWall, self.distLookahead)
		heading = ha - hd
		return heading