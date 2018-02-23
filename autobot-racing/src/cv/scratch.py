import numpy as np
import cv2

class ComputerVision:
	ALLOWED_COLORS = (
		(255, 0, 0),
		(0, 255, 0),
		(0, 0, 255),
	)

	def __init__(self, videoDevice=0):
		self.cap = cv2.VideoCapture(videoDevice)

	def run(self, showFrame=True):
		while(True):
			# Capture frame-by-frame
			ret, frame = self.cap.read()
			height, width = frame.shape[:2]
			area = height * width

			# Preprocess the image.
			# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# ret,thresh = cv2.threshold(gray,120,255,0)
			blurred = cv2.GaussianBlur(frame, (5, 5), 0)
			gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
			lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
			thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
			
			# Find all contours.
			im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

			# Loop over candidate contours.
			candidates = list(filter(self.checkArea, contours))
			# cv2.drawContours(frame, contours, -1, (0,0,255), 1)
			for c in candidates:
				epsilon = 0.03 * cv2.arcLength(c, True)
				approx = cv2.approxPolyDP(c, epsilon, True)
				
				# Check its triangley-ness.
				if len(approx) != 3:
					continue
				if not self.checkTriangle(approx):
					continue
				
				# Determine color.
				M = cv2.moments(c)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				
				color = (int(frame[cY][cX][0]), int(frame[cY][cX][1]), int(frame[cY][cX][2]))
				color = self.getClosestColor(color)
				# mask = np.zeros(frame.shape,np.uint8)
				# cv2.drawContours(mask, [c], 0, 255, -1)
				# color = cv2.mean(frame, mask = mask)
				# print("GOT COLOR: " + str(color))
			 
				cv2.drawContours(frame, [approx], -1, color, 3)
				
				# draw the contour and center of the shape on the image
				cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
				label = "(" + str(cX) + "," + str(cY) + ")"
				cv2.putText(frame, label, (cX - 20, cY - 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
				

			if showFrame:
				# display = np.dstack((frame, gray))
				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
		
		# Cleanup. TODO: Move this elsewhere
		self.cap.release()
		cv2.destroyAllWindows()
	
	def checkArea(self, contour):
		a = cv2.contourArea(contour)
		return a > 50 and a < 20000
		
	def npDistance(self, a, b):
		return np.linalg.norm(a-b)
		
	def getClosestColor(self, color):
		def distance(c1, c2):
			(r1,g1,b1) = c1
			(r2,g2,b2) = c2
			return ((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2) ** 0.5
		closest = sorted(self.ALLOWED_COLORS, key=lambda c: distance(c, color))
		return closest[0]
		
	def checkTriangle(self, contour):
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
		if abs(ratio - 0.363636) >= 0.07:
			return False
		return True
		
ComputerVision().run()