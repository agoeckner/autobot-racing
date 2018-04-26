import numpy as np
from numpy.linalg import *

# Takes a point (x,y) and determines if it is within a polygon.
def isPointInPolygon(polygon, point):
	inArea = False
	n = len(polygon) - 1
	i = 0
	for vertex in polygon:
		if ((vertex[1] < point[1] and polygon[n][1] >= point[1]) or
			(polygon[n][1] < point[1] and vertex[1] >= point[1])):
			if (vertex[0] + (point[1] - vertex[1]) /
				(polygon[n][1] - vertex[1]) *
				(polygon[n][0] - vertex[0]) < point[0]):
				inArea = not inArea
		n = i
		i += 1
	return inArea

# Returns the length of the longest wall in a polygon.
def getPolygonMaxEdgeLen(polygon):
	maxLen = 0
	p1 = polygon[0]
	for p in range(1, len(polygon)):
		p2 = polygon[p]
		d = np.linalg.norm(np.array(p1) - np.array(p2))
		print("d: " + str(d))
		if d > maxLen:
			maxLen = d
		p1 = p2
	return maxLen

def euclideanDistance(a, b):
	return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5