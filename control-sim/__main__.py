from random import random
from math import *
import numpy as np
from numpy.linalg import *
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
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
		((wall0, wall1), d) = self._getClosestPolyVertex(pos, self.innerWall)
		heading = atan2(wall1[1] - wall0[1], wall1[0] - wall0[0]) + pi
		# print("CURRENTLY " + str(d) + " FROM THE WALL, HEADING " + str(heading))
		return heading
	
	# Returns the desired speed at a specific position on the track.
	def getDesiredSpeed(self, pos):
		pass
	
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
		

class SimDisplay(Widget):
	FUTURE_LINE_SCALE = 100

	def __init__(self, track, **kwargs):
		super(SimDisplay, self).__init__(**kwargs)
		
		self.track = track
		self.traj = {}
	
	def on_step(self, vehicle):
		# Reset canvas.
		self.canvas.clear()
		
		# Display the track.
		color = (0, 0, 0, 1)
		with self.canvas:
			Color(*color, mode='rgba')
			self.innerWall = Line(points=self.track.innerWall, width=2.0)
			self.outerWall = Line(points=self.track.outerWall, width=3.0)
		
		# Trajectory line.
		pos = vehicle.position
		futurePoint = (pos[0] + cos(vehicle.heading) * vehicle.speed * self.FUTURE_LINE_SCALE,
			pos[1] + sin(vehicle.heading) * vehicle.speed * self.FUTURE_LINE_SCALE)
		with self.canvas:
			Color(1, 0, 0, 1, mode='rgba')
			if vehicle not in self.traj or self.traj[vehicle] == None:
				self.traj[vehicle] = Line(points=pos, width=1.5)
			else:
				self.traj[vehicle] = Line(points=self.traj[vehicle].points + pos, width=1.5)
			
			# Future trajectory.
			Color(0, 1, 0, 1, mode='rgba')
			Line(points=[pos, futurePoint], width=1.2)
			
			# Vehicle dot.
			Color(0, 0, 0, 1, mode='rgba')
			d = 5.
			Ellipse(pos=(pos[0] - d / 2, pos[1] - d / 2), size=(d, d), width=5)


class SimTrack:
	def __init__(self, innerWall, outerWall):
		self.innerWall = innerWall
		self.outerWall = outerWall
			
class SimVehicle:
	MIN_TURN_ANGLE = pi / 24

	def __init__(self, initialPosition, initialHeading, initialSpeed):
		self.initialPosition = initialPosition
		self.initialHeading = initialHeading
		self.initialSpeed = initialSpeed
		self.position = initialPosition
		self.heading = initialHeading
		self.speed = initialSpeed
	
	def reset(self):
		self.position = self.initialPosition
		self.heading = self.initialHeading
		self.speed = self.initialSpeed
	
	def updateHeading(self, delta):
		# print("DELTA: " + str(delta))
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
		Clock.schedule_interval(self.step, 1 / 10)
		
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
		for vehicle in self.vehicles:
			self.display.traj[vehicle] = None
			vehicle.reset()
	
	def step(self, dt):
		for vehicle in self.vehicles:
			# Move the vehicle.
			vehicle.position[0] += cos(vehicle.heading) * vehicle.speed
			vehicle.position[1] += sin(vehicle.heading) * vehicle.speed
			self.display.on_step(vehicle)
			
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