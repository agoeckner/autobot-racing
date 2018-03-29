from pykinect import nui
import numpy as np
import cv2
import math
from math import pi

class ComputerVision:
	# The allowed vehicle colors.
	ALLOWED_COLORS = (
		(255, 0, 0),
		(0, 255, 0),
		(0, 0, 255),
		# (255, 0, 255),
	)
	
	# Used as a tuning constant for the epsilon value of approxPolyDP.
	APPROX_ARCLEN_MULTIPLIER = 0.03
	
	# The boundary sizes (in pixels squared) of contours that are acceptable
	# for further processing.
	CONTOUR_AREA_MIN = 30
	CONTOUR_AREA_MAX = 20000
	
	# The actual, measured ratio of the triangle targets placed on the vehicles.
	TRIANGLE_RATIO = 0.48507125007 #0.363636
	
	# The tolerance used to check if triangles conform to TRIANGLE_RATIO.
	TRIANGLE_RATIO_TOLERANCE = 0.06
	
	
	# Initializes the computer vision system. Set videoDevice to 0 for camera, -1 for Kinect.
	def __init__(self, queue, videoDevice = -1):
		self.queue = queue
	
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
		else:
			self.mode = "CAMERA"
			# Open video device.
			self.cap = cv2.VideoCapture(videoDevice)
		
			# Test the camera.
			ret, frame = self.cap.read()
			if not ret:
				raise CameraException("Unable to read from video device.")
	
	# Closes all devices, etc. This function should be called when done with CV.
	def close(self):
		if self.mode == "KINECT":
			self.kinect.close()
		else:
			self.cap.release()
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

				if not self.processFrame(frame):
					break
		else:
			# Start the Kinect stream.
			try:
				self.kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
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
		self.processFrame(video)
	
	def processFrame(self, frame, showFrame = True):
		# Preprocess the image.
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# ret,thresh = cv2.threshold(gray,120,255,0)
		blurred = cv2.GaussianBlur(frame, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
		
		# Find all contours.
		im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
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
			
			# Get the position of the triangle center.
			M = cv2.moments(approx)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			center = (cX, cY)
			
			# Get the heading of the triangle.
			heading = self.getTriangleHeading(approx)

			# Determine color of the pixel at the center of the contour.
			pixel = frame[cY][cX]
			color = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
			color = self.getClosestColor(color)
			
			# Push the data out to the main thread.
			if self.queue != None:
				self.queue.push((center, heading, color))
		 
			# Draw the contour and center of the shape on the image.
			if showFrame:
				cv2.drawContours(frame, [approx], -1, color, 3)
				cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
				label = "({:d}, {:d}), {:.2f}".format(cX, cY, math.degrees(heading))
				cv2.putText(frame, label, (cX - 20, cY - 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

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
		
		# Get slope of shortest side.
		diff = np.subtract(short[1], short[0])[0]
		
		# Get heading.
		heading = np.arctan2(diff[0], diff[1])
		
		return heading		
	
	# Checks that the contour area is within acceptable bounds.
	def checkContourArea(self, contour):
		a = cv2.contourArea(contour)
		return a > self.CONTOUR_AREA_MIN and a < self.CONTOUR_AREA_MAX

class CameraException(Exception):
	pass

if __name__ == "__main__":
	# Debug mode
	ComputerVision(None).run(showFrame=True)