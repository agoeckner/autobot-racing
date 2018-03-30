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

def euclideanDistance(a, b):
	return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5