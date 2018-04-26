try:
	from pykinect import nui
except ImportException:
	print("WARN: Running without Kinect support!")
import numpy as np
import cv2
import math
from math import pi
import time
import random

class ComputerVision:
	# The allowed vehicle colors.
	ALLOWED_COLORS = (
		(255, 0, 0),
		(0, 255, 0),
		(0, 0, 255),
		# (255, 0, 255),
	)
	
	# Used to determine the cutoff for black/white
	# WHITE_THRESHOLD = 160 #FOR RECORDED VIDEO
	WHITE_THRESHOLD = 110 #FOR REAL-TIME
	
	# Used as a tuning constant for the epsilon value of approxPolyDP.
	APPROX_ARCLEN_MULTIPLIER = 0.11
	
	# The boundary sizes (in pixels squared) of contours that are acceptable
	# for further processing.
	CONTOUR_AREA_MIN = 100
	CONTOUR_AREA_MAX = 300
	
	# The actual, measured ratio of the triangle targets placed on the vehicles.
	TRIANGLE_RATIO = 0.48507125007 #0.363636
	
	# The tolerance used to check if triangles conform to TRIANGLE_RATIO.
	TRIANGLE_RATIO_TOLERANCE = 0.5 #0.1
	
	
	# Initializes the computer vision system. Set videoDevice to 0 for camera, -1 for Kinect.
	def __init__(self, parent, videoDevice = 0):
		self.parent = parent
		self.getTrack = True
		self.trackOut = []
		self.trackIn = []
		self.startLine = []
		self.startLine2 = []
		
		if parent != None:
			self.queue = parent.telemetryQueue
		
		# Set up FPS counter.
		self.lastFrameTime = time.time()
	
		# Run in Kinect mode.
		if videoDevice == -1:
			print("Initializing Kinect")
			self.mode = "KINECT"
			try:
				self.kinect = nui.Runtime()
				self.kinect.video_frame_ready += self._processKinectFrame
			except OSError as e:
				print("OOPS: " + str(e))
				raise e
		
		elif videoDevice is 2:
			self.mode = "CAMERA"
			self.cap = cv2.VideoCapture('C:\\Users\\Harold\\Documents\\Programming\\Autobot-Racing\\autobot-racing\\track.avi')
		else:
			self.mode = "CAMERA"
			# Open video device.
			self.cap = cv2.VideoCapture(videoDevice)
		
			# Test the camera.
			ret, frame = self.cap.read()
			if not ret:
				raise CameraException("Unable to read from video device.")
		#self.out = cv2.VideoWriter('motion.avi', -1, 20.0, (640,480))
	
	# Closes all devices, etc. This function should be called when done with CV.
	def close(self):
		print("CLOSE COMPUTER VISION STREAM")
		if self.mode == "KINECT":
			self.kinect.close()
		else:
			self.cap.release()
		print("Closed")
		#self.out.release()
		cv2.destroyAllWindows()

	# The primary computer vision system loop. This polls the camera as fast as
	# possible, processing each frame and sending the data to other modules.
	def run(self, showFrame = False):
	
		if self.mode == "CAMERA":
			while(True):
				# Capture frame-by-frame
				ret, frame = self.cap.read()
				if not ret:
					raise CameraException("Unable to read from video device.")
				height, width = frame.shape[:2]

				if self.getTrack is True:
					self.findTrack(frame)
				
				if not self.processFrame(frame):
					break
		else:
			# Start the Kinect stream.
			try:
				print("Opening Kinect stream")
				self.kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
				print("Opened Kinect stream")
			except OSError as e:
				print("OOPS2: " + str(e))
				raise e
			
			while True:
				key = cv2.waitKey(1)
				if key == 27: break
		
		# Shut down the CV system.
		self.close()
	
	def _processKinectFrame(self, frame):
		video = np.empty((480,640,4),np.uint8)
		frame.image.copy_bits(video.ctypes.data)
		#self.out.write(video)
		
		
		if self.getTrack is True:
			self.findTrack(video)
		else:
			self.processFrame(video)
	
	##-----------------------------------------------------------------------------
	## Identifies the track and creates a start line
	##-----------------------------------------------------------------------------
	def findTrack(self, frame): #{
		candidate = None
		sizeList = []
		blurred = cv2.GaussianBlur(frame, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		#lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)[1]
		
		# Find all contours.
		im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
			cv2.CHAIN_APPROX_NONE)

		contours.sort(key=lambda x:cv2.arcLength(x, True), reverse=True)
		#cv2.drawContours(frame, contours, -1, (255,0,0), 1)
		
		#Grab the two biggest contours in the frame
		candidate = contours[1]
		##TODO: From 3 to 2-------------------------------------------------------------------------------------------------
		candidate1 = contours[2]
		#print(candidate)
		#print('Candidate: '+str(candidate))
		if candidate is not None:
			epsilon = 0.03 * cv2.arcLength(candidate, True)
			approx = cv2.approxPolyDP(candidate, epsilon, True)
			#cv2.drawContours(frame, [approx], -1, (0,255,0), 2)

			epsilon = 0.02 * cv2.arcLength(candidate1, True)
			approx1 = cv2.approxPolyDP(candidate1, epsilon, True)
			#cv2.drawContours(frame, [approx1], -1, (0,255,0), 2)
			#self.parent.UIQueue.q.put(('CamFeed', frame))
			#print(approx)
			#print(approx1)

		outer = []
		for t in approx:
			outer.append(tuple(t[0]))
		outer.append(outer[0])
		inner = []
		for t in approx1:
			#cv2.putText(frame, str(tuple(t[0])), tuple(t[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
			inner.append(tuple(t[0]))
		inner.append(inner[0])
		print(inner)
		# inner.reverse()
		#TODO: pass this garbage through the queue for the main thread
		#Pass the outer track then the inner
		self.parent.trackQueue.put(inner)
		self.parent.trackQueue.put(outer)
		self.trackIn = approx
		self.trackOut = approx1

		#Create a start line
		innerValues = []
		lengths = []
		#print(approx1)
		#print(inner)
		for i in range(0, len(inner)):
			if (i+1) != len(inner):
				point1 = inner[i]
				point2 = inner[i+1]
				x = abs(point1[0] - point2[0])
				y = abs(point1[1] - point2[1])
				x2 = x*x
				y2 = y*y
				lineD = x2 + y2
				length = math.sqrt(lineD)
				lengths.append(length)
				
				innerValues.append([point1, point2])
		
		maxLength = -1
		lineSide = []
		for i in range(0,len(lengths)):
			l = lengths[i]
			#print(l)
			#print(innerValues[i])
			if l > maxLength:
				maxLength = l
				lineSide = innerValues[i]
		
		#print(maxLength)
		#print(lineSide)
		
		midPointX = (lineSide[0][0] + lineSide[1][0]) / 2
		midPointY = (lineSide[0][1] + lineSide[1][1]) / 2
		midPoint = [midPointX, midPointY]
		
		midPoint[0] = int(round(midPoint[0]))
		midPoint[1] = int(round(midPoint[1]))
		#print(midPoint)
		#print(tuple(midPoint))
		
		outerLine = self._getClosestPolyEdge(midPoint, outer)
		outerPoints = outerLine[0]
		
		#print(outerLine)
		#print(outerPoints)
		
		#Find the closest point on the outer line
		outerA = outerPoints[0]
		outerB = outerPoints[1]
		#print(outerA)
		#print(outerB)
		aToMid = [midPointX - outerA[0], midPointY - outerA[1]]
		aToB = [outerB[0] - outerA[0], outerB[1] - outerB[1]]
		
		aToBMag = (aToB[0] * aToB[0]) + (aToB[1]*aToB[1])
		#print(aToBMag)
		aMidDotaB = (aToMid[0]*aToB[0]) + (aToMid[1]*aToB[1])
		#print(aMidDotaB)
		normDist = aMidDotaB / aToBMag
		
		outPointX = (outerA[0] + aToB[0]*normDist)
		outPointY = outerA[1] + aToB[1]*normDist
		#print(outPointX)
		#print(outPointY)
		outPoint = [outPointX, outPointY]
		outPoint[0] = int(round(outPoint[0]))
		outPoint[1] = int(round(outPoint[1]))
		#print(outPoint)
		#outerXMid = (outerPoints[0][0] + outerPoints[1][0]) / 2
		#outerYMid = (outerPoints[0][1] + outerPoints[1][1]) / 2
		#outerMidPoint = [outerXMid, outerYMid]
		#outerMidPoint[0] = int(round(outerMidPoint[0]))
		#outerMidPoint[1] = int(round(outerMidPoint[1]))
		
		#cv2.line(frame, tuple(midPoint), tuple(outPoint), (255,0,0), 2)
		#cv2.line(frame, tuple(outPoint), tuple(outPoint), (255,0,0), 15)
		
		midPoint2 = [midPoint[0]+25, midPoint[1]]
		outPoint2 = [outPoint[0]+25, outPoint[1]]
		self.startLine = [midPoint, outPoint]
		self.startLine2 = [midPoint2, outPoint2]
		##TODO: Remove the drawing of the second set of points for the rectangle---------------------------------------------------
		#cv2.line(frame, tuple(midPoint2), tuple(outPoint2), (255,0,0), 2)
		lapPoly = [tuple(outPoint), tuple(midPoint), tuple(midPoint2), tuple(outPoint2), tuple(outPoint)]
		#print(lapPoly)
		
		self.parent.trackQueue.put(outer)
		if random.random() < 0.5:
			self.parent.UIQueue.q.put(('CamFeed', frame))
		self.getTrack = False
		self.parent.getTrack = True
		
		
		#cv2.imshow('frame', frame)
		#while True:
		#	key = cv2.waitKey(1)
		#	if key == 27: break
	#}
	
	def processFrame(self, frame, showFrame = False, draw = True):
		# Preprocess the image.
		blurred = cv2.GaussianBlur(frame, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, self.WHITE_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
		
		# Find all contours.
		im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
			cv2.CHAIN_APPROX_NONE)

		# Loop over candidate contours (those that meet size limits).
		candidates = list(filter(self.checkContourArea, contours))
		for c in candidates:
			epsilon = self.APPROX_ARCLEN_MULTIPLIER * cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, epsilon, True)
			
			# Check its triangley-ness.
			if len(approx) != 3:
				continue
			# Check proportions of the triangle.
			if not self.checkTriangleProportions(approx):
				continue
			# cv2.drawContours(frame, [c], -1, (0,255,0), 2)
			
			# Get the position of the triangle center.
			M = cv2.moments(approx)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			center = (cX, cY)
			
			# Get the heading of the triangle.
			heading = self.getTriangleHeading(approx)

			# Determine color of the pixel at the center of the contour.
			totalR = 0
			totalG = 0
			totalB = 0
			for x in range(cX - 1, cX + 2):
				for y in range(cY - 1, cY + 2):
					pixel = frame[y][x]
					totalR += int(pixel[2])
					totalG += int(pixel[1])
					totalB += int(pixel[0])
			
			
			# This is the color in normal format, RGB.
			color = (totalR / 9.0, totalG / 9.0, totalB / 9.0)
			color = self.getClosestColor(color)
			
			# This is the color in OpenCV format, BGR
			colorCV = (color[2], color[1], color[0])
			
			# Push the data out to the main thread.
			if self.parent != None:
				self.queue.put((center, heading, color))
		 
			# Draw the contour and center of the shape on the image.
			if draw:
				cv2.drawContours(frame, [approx], -1, colorCV, 3)
				cv2.circle(frame, (cX, cY), 6, (255, 255, 255), -1)
				label = "({:d}, {:d}), {:.2f}".format(cX, cY, math.degrees(heading))
				# label = str(cv2.contourArea(c))
				cv2.putText(frame, label, (cX - 20, cY - 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		
		if draw:
			# Do FPS label
			current = time.time()
			diff = current - self.lastFrameTime
			if diff == 0:
				label = "FPS: ?"
			else:
				fps = 1 / (current - self.lastFrameTime)
				self.lastFrameTime = current
				label = "FPS: {:.2f}".format(fps)
			cv2.putText(frame, label, (5, 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

		if len(self.trackIn) > 0:
			cv2.drawContours(frame, [self.trackIn], -1, (0,255,0), 2)
		if len(self.trackOut) > 0:
			cv2.drawContours(frame, [self.trackOut], -1, (0,255,0), 2)
		if len(self.startLine) > 0:
			cv2.line(frame, tuple(self.startLine[0]), tuple(self.startLine[1]), (255,0,0), 2)
			cv2.line(frame, tuple(self.startLine2[0]), tuple(self.startLine2[1]), (255,0,0), 2)
		#Put the frame in the queue for the UI
		if self.parent != None:
			self.parent.UIQueue.q.put(('CamFeed', frame))

		if showFrame:
			# display = np.dstack((frame, gray))
			cv2.imshow('frame', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				return False
		return True
	
	# Identifies detected vehicles and acts on that information.
	def processVehicle(self, color, position, heading):
		pass
	
	# Uses NumPy to find the distance between two NumPy points.
	def npDistance(self, a, b):
		return np.linalg.norm(a-b)
	
	# Returns the closest allowable color to the specified color.
	def getClosestColor(self, color):
		def distance(c1, c2):
			(r1,g1,b1) = c1
			(r2,g2,b2) = c2
			return ((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2) ** 0.5
		closest = min(self.ALLOWED_COLORS, key=lambda c: distance(c, color))
		return closest
	
	# Checks that proportions of the triangle are within acceptable bounds.
	def checkTriangleProportions(self, contour):
		# Get the sides.
		sides = ((contour[0], contour[1]),
			(contour[1], contour[2]),
			(contour[2], contour[0]))
		
		# Get lengths of each side.
		lengths = [self.npDistance(s[0], s[1]) for s in sides]

		# Determine which is shortest side.
		minLen = 999999
		minLenIdx = -1
		for idx in range(0, len(lengths)):
			l = lengths[idx]
			if l < minLen:
				minLen = l
				minLenIdx = idx
		if minLenIdx == -1:
			return False
		
		# Check that two longer sides are roughly equal.
		long1 = None
		for idx in range(0, len(lengths)):
			if idx != minLenIdx:
				if long1 == None:
					long1 = lengths[idx]
				else:
					long2 = lengths[idx]
		if abs(long1 - long2) >= 5:
			return False
			
		ratio = minLen / max(lengths)
		if abs(ratio - self.TRIANGLE_RATIO) >= self.TRIANGLE_RATIO_TOLERANCE:
			return False
		return True
	
	# Determines the heading in which a triangle is pointing.
	def getTriangleHeading(self, triangle):
		# Get the sides.
		sides = ((triangle[0], triangle[1]),
			(triangle[1], triangle[2]),
			(triangle[2], triangle[0]))
		oppositePoint = {
			0: 2,
			1: 0,
			2: 1
		}
		
		# Get lengths of each side.
		lengths = [self.npDistance(s[0], s[1]) for s in sides]

		# Determine which is shortest side.
		minLen = 999999
		minLenIdx = -1
		for idx in range(0, len(lengths)):
			l = lengths[idx]
			if l < minLen:
				minLen = l
				minLenIdx = idx
		short = sides[minLenIdx]
		
		# Get midpoint of shortest side.
		mid = (short[0] + short[1]) / 2
		
		# Get slope from midpoint of short line to opposite point.
		opp = triangle[oppositePoint[minLenIdx]]
		diff = mid - opp
		diff = [diff[0][0], -diff[0][1]]
		
		# Get heading.
		heading = np.arctan2(diff[0], diff[1]) + pi / 2
		
		return heading		
	
	# Checks that the contour area is within acceptable bounds.
	def checkContourArea(self, contour):
		a = cv2.contourArea(contour)
		return a > self.CONTOUR_AREA_MIN and a < self.CONTOUR_AREA_MAX

	
	def _getClosestPolyEdge(self, pos, polygon):
		def point_to_line_dist(p1, p2, pos):
			"""Calculate the distance between a point and a line segment.

			To calculate the closest distance to a line segment, we first need to check
			if the point projects onto the line segment.  If it does, then we calculate
			the orthogonal distance from the point to the line.
			If the point does not project to the line segment, we calculate the 
			distance to both endpoints and take the shortest distance.

			:param point: Numpy array of form [x,y], describing the point.
			:type point: numpy.core.multiarray.ndarray
			:param line: list of endpoint arrays of form [P1, P2]
			:type line: list of numpy.core.multiarray.ndarray
			:return: The minimum distance to a point.
			:rtype: float
			"""
			
			point = np.array(pos)
			line = [np.array(p1), np.array(p2)]
			
			# unit vector
			unit_line = line[1] - line[0]
			norm_unit_line = unit_line / np.linalg.norm(unit_line)

			# compute the perpendicular distance to the theoretical infinite line
			segment_dist = (
				np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
				np.linalg.norm(unit_line)
			)
			
			diff = (
				(norm_unit_line[0] * (point[0] - line[0][0])) + 
				(norm_unit_line[1] * (point[1] - line[0][1]))
			)

			x_seg = (norm_unit_line[0] * diff) + line[0][0]
			y_seg = (norm_unit_line[1] * diff) + line[0][1]

			endpoint_dist = min(
				np.linalg.norm(line[0] - point),
				np.linalg.norm(line[1] - point)
			)

			# decide if the intersection point falls on the line segment
			lp1_x = line[0][0]  # line point 1 x
			lp1_y = line[0][1]  # line point 1 y
			lp2_x = line[1][0]  # line point 2 x
			lp2_y = line[1][1]  # line point 2 y
			is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
			is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
			
			if is_betw_x and is_betw_y:
				return (segment_dist, False)
			else:
				# if not, then return the minimum distance to the segment endpoints
				return (endpoint_dist, True)
			
		def dist(A, B, C):
			"""Calculate the distance of point C to line segment spanned by points A, B.
			"""

			a = np.asarray(A)
			b = np.asarray(B)
			c = np.asarray(C)
			#project c onto line spanned by a,b but consider the end points
			#should the projection fall "outside" of the segment    
			n, v = b - a, c - a
			#the projection q of c onto the infinite line defined by points a,b
			#can be parametrized as q = a + t*(b - a). In terms of dot-products,
			#the coefficient t is (c - a).(b - a)/( (b-a).(b-a) ). If we want
			#to restrict the "projected" point to belong to the finite segment
			#connecting points a and b, it's sufficient to "clip" it into
			#interval [0,1] - 0 corresponds to a, 1 corresponds to b.
			t = max(0, min(np.dot(v, n)/np.dot(n, n), 1))
			return np.linalg.norm(v - t*n)
		
		closest = ()
		setPrevClosest = False
		minD = 99999999
		# print("START FOR POLY: " + str(polygon))
		# print("CHECK AT POINT: " + str(pos))
		
		p1 = polygon[0]
		for p in range(1, len(polygon)):
			p2 = polygon[p]
			(d, outside) = point_to_line_dist(p1, p2, pos)
			if not outside or  (p1, p2) != self.prevClosest:
				if d < minD:
					minD = d
					setPrevClosest = not outside
					closest = (p1, p2)
			p1 = p2

		if setPrevClosest:
			self.prevClosest = closest
		return (closest, abs(minD))
		
class CameraException(Exception):
	pass

if __name__ == "__main__":
	# Debug mode
	cv = ComputerVision(None, 2)#"motion.avi")#"output.avi")
	try:
		cv.run(showFrame=True)
	except KeyboardInterrupt as e:
		cv.close()
