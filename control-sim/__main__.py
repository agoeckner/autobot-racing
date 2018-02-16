from random import random
from math import *
import numpy as np
from numpy.linalg import *
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

Window.clearcolor = (1, 1, 1, 1)

class ControlSystem:
	def __init__(self):
		pass

	# Given an actual and a desired heading, returns new delta heading value.
	def heading(self, actual, desired):
		return desired - actual
	
	# Given an actual and a desired throttle, returns new delta speed value.
	def throttle(self, actual, desired):
		return 0 #TODO

class GuidanceSystem:
	def __init__(self, track):
		self.innerWall = track.innerWall
	
	# Returns the desired heading at a specific position on the track.
	def getDesiredHeading(self, pos):
		(wall0, wall1) = self._getClosestPolyVertex(pos, self.innerWall)
		heading = atan2(wall1[1] - wall0[1], wall1[0] - wall0[0]);
		# print("CLOSEST LINE "+str(pos)+": " + str((wall0, wall1)))
		# print("HEADING: " + str(heading))
		return heading
	
	# Returns the desired speed at a specific position on the track.
	def getDesiredSpeed(self, pos):
		pass
	
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
		return closest
		

class SimDisplay(Widget):
	def __init__(self, track, **kwargs):
		super(SimDisplay, self).__init__(**kwargs)
		
		self.trajectory = None
		
		# Display the track.
		color = (0, 0, 0, 1)
		with self.canvas:
			Color(*color, mode='rgba')
			self.innerWall = Line(points=track.innerWall)
			self.outerWall = Line(points=track.outerWall, width=2.0)
		
		# # Create the trajectory line.
		# color = (1, 0, 0, 1)
		# with self.canvas:
			# Color(*color, mode='rgba')
			# d = 30.
			# Ellipse(pos=(50 - d / 2, 50 - d / 2), size=(d, d))
			# print("Added elipse")
	
	def on_step(self, pos):
		if pos == None:
			pos = self.center
		
		# Trajectory line.
		with self.canvas:
			Color(1, 0, 0, 1, mode='rgba')
			if self.trajectory == None:
				self.trajectory = Line(points=pos)
				d = 10.
				Ellipse(pos=(pos[0] - d / 2, pos[1] - d / 2), size=(d, d), width=5)
			else:
				# d = 5.
				# Ellipse(pos=(pos[0] - d / 2, pos[1] - d / 2), size=(d, d))
				self.trajectory = Line(points=self.trajectory.points + pos)

class SimTrack:
	def __init__(self, innerWall, outerWall):
		self.innerWall = innerWall
		self.outerWall = outerWall
			
class SimVehicle:
	MIN_TURN_ANGLE = pi / 6

	def __init__(self, initialPosition, initialHeading, initialSpeed):
		self.position = initialPosition
		self.heading = initialHeading
		self.speed = initialSpeed
	
	def updateHeading(self, delta):
		print("DELTA: " + str(delta))
		delta = delta % pi
		if delta > 0:
			self.heading += min(delta, self.MIN_TURN_ANGLE)
		else:
			self.heading -= min(delta, self.MIN_TURN_ANGLE)
	
	def updateSpeed(self, delta):
		self.speed += delta

class ControlSim(App):

	def build(self):
		# Set up simulation.
		self.initSim()
	
		# Set up UI.
		parent = Widget()
		self.display = SimDisplay(self.track)
		restartBtn = Button(text='Restart')
		restartBtn.bind(on_release=self.restart)
		parent.add_widget(self.display)
		parent.add_widget(restartBtn)
		
		# Set up event loop.
		Clock.schedule_interval(self.step, 1 / 30)
		
		return parent
	
	def initSim(self):
		# Add the vehicle.
		self.vehicles = [SimVehicle([250,250], pi / 2, 5)]
		
		# Add the track.
		self.track = SimTrack(
			[(200, 220), (600, 220), (600, 150), (200, 150), (200, 220)],
			[(100, 320), (700, 320), (700, 50), (100, 50), (100, 320)])
		
		# Set up control/guidance system.
		self.guidance = GuidanceSystem(self.track)
		self.control = ControlSystem()

	def restart(self, obj):
		self.display.canvas.clear()
		raise Exception("not implemented")
	
	def step(self, dt):
		for vehicle in self.vehicles:
			# Move the vehicle.
			vehicle.position[0] += cos(vehicle.heading) * vehicle.speed
			vehicle.position[1] += sin(vehicle.heading) * vehicle.speed
			self.display.on_step(vehicle.position)
			
			# Determine guidance.
			desiredHeading = self.guidance.getDesiredHeading(vehicle.position)
			desiredSpeed = self.guidance.getDesiredSpeed(vehicle.position)
			
			# Run control algorithm.
			deltaHeading = self.control.heading(vehicle.heading, desiredHeading)
			deltaSpeed = self.control.throttle(vehicle.speed, desiredSpeed)
			
			# Apply changes to vehicle.
			vehicle.updateHeading(deltaHeading)
			vehicle.updateSpeed(deltaSpeed)
		return True #false to stop

if __name__ == '__main__':
	ControlSim().run()