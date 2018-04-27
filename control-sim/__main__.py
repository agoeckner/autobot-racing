from random import randint, random
from math import *
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
import time

# Import control/guidance modules from the actual program.
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], "..", "autobot-racing"))
import controls as ngc
import Utilities

Window.clearcolor = (1, 1, 1, 1)

class SimDisplay(Widget):
	FUTURE_LINE_SCALE = 100

	def __init__(self, parent, track, **kwargs):
		super(SimDisplay, self).__init__(**kwargs)
		
		self.tempHeadingLine = None
		self.par = parent
		self.track = track
		self.traj = {}
	
	def on_touch_down(self, touch):
		pos = (touch.x, touch.y)
		print("LOCATION: " + str(pos))
		
		heading = self.par.vehicles[0].guidance.getDesiredHeading(pos)
		# print("   HEADING: " + str(degrees(heading)))
		
		self.draw_trajectory(pos, heading)
	
	def on_touch_move(self, touch):
		pos = (touch.x, touch.y)
		heading = self.par.vehicles[0].guidance.getDesiredHeading(pos)
		self.draw_trajectory(pos, heading)
	
	def on_touch_up(self, touch):
		self.tempHeadingLine = None
	
	def draw_trajectory(self, pos, heading):
		# Future trajectory.
		futurePoint = (pos[0] + cos(heading) * 60,
			pos[1] + sin(heading) * 60)
		self.tempHeadingLine = [pos, futurePoint]
	
	def on_step(self, vehicles):
		# Reset canvas.
		self.canvas.clear()
		
		# Display the track.
		color = (0, 0, 0, 1)
		thl = self.tempHeadingLine
		with self.canvas:
			Color(*color, mode='rgba')
			self.innerWall = Line(points=self.track.innerWall, width=2.0)
			self.outerWall = Line(points=self.track.outerWall, width=3.0)
			
			# Draw temporary heading line.
			if thl != None:
				Color(1, 0, 1, 1, mode='rgba')
				Line(points=self.tempHeadingLine, width=1.6)
		
		# Trajectory lines.
		for vehicle in vehicles:
			pos = vehicle.position
			futurePoint = (pos[0] + cos(vehicle.heading) * vehicle.actualSpeed * self.FUTURE_LINE_SCALE,
				pos[1] + sin(vehicle.heading) * vehicle.actualSpeed * self.FUTURE_LINE_SCALE)
			with self.canvas:
				Color(*vehicle.color, mode='rgba')
				if vehicle not in self.traj or self.traj[vehicle] == None:
					self.traj[vehicle] = Line(points=pos, width=1.5)
				else:
					self.traj[vehicle] = Line(points=self.traj[vehicle].points + pos, width=1.5)
				
				# Future trajectory.
				Color(0, 1, 1, 1, mode='rgba')
				Line(points=[pos, futurePoint], width=1.2)
				
				# Vehicle dot.
				Color(0, 0, 0, 1, mode='rgba')
				d = 10. #5.
				Ellipse(pos=(pos[0] - d / 2, pos[1] - d / 2), size=(d, d), width=5)

class SimTrack:
	def __init__(self, innerWall, outerWall):
		self.innerWall = innerWall
		# self.innerWall.reverse() # TODO: TEMPORARY REVERSAL
		self.outerWall = outerWall
		self.longestStraightaway = Utilities.getPolygonMaxEdgeLen(self.innerWall)

class SimVehicleManager:
	def __init__(self, environment):
		self.environment = environment
		self.vehicles = []
	
	def addVehicle(self, vehicle): #*args, **kwargs):
		# vehicle = SimVehicle(args, kwargs)
		vehicle.guidance.vehicle = vehicle
		self.vehicles.append(vehicle)

	def __getitem__(self, index):
		return self.vehicles[index]

class SimVehicle:
	# Turning radius measured to be ~1.5 feet
	# TODO: Properly implement turning radius.
	MIN_TURN_ANGLE = pi / 22

	def __init__(self, initialPosition, initialHeading, initialSpeed,
			control, guidance, color = (1, 0, 0, 1)):
		self.initialPosition = initialPosition
		self.initialHeading = initialHeading
		self.initialSpeed = initialSpeed
		self.position = initialPosition
		self.heading = initialHeading
		self.actualSpeed = initialSpeed
		self.color = color
		self.control = control
		self.guidance = guidance
	
	def reset(self):
		self.position = self.initialPosition
		self.heading = self.initialHeading
		self.actualSpeed = self.initialSpeed
	
	def updateHeading(self, delta):
		if abs(delta) >= 0.087:
			# Clamp the turn rate.
			if delta > 0:
				self.heading += self.MIN_TURN_ANGLE #min(delta, self.MIN_TURN_ANGLE)
			else:
				self.heading += -self.MIN_TURN_ANGLE #max(delta, -self.MIN_TURN_ANGLE)
			
			# Clamp the heading.
			self.heading = self.heading % (2 * pi)
	
	def updateSpeed(self, delta):
		self.actualSpeed += delta

class ControlSim(App):

	def build(self):
		# Set up simulation.
		self.initSim()
	
		# Set up UI.
		parent = Widget()
		self.display = SimDisplay(self, self.track)
		restartBtn = Button(text='Restart')
		restartBtn.bind(on_release=self.restart)
		parent.add_widget(self.display)
		parent.add_widget(restartBtn)
		
		# Set up event loop.
		Clock.schedule_interval(self.step, 1 / 50)
		
		return parent
	
	def initSim(self):
		# Add the track.
		inner = [(356, 154), (357, 252), (183, 257), (180, 155), (356, 154)]
		inner.reverse()
		self.track = SimTrack(
			# NORMAL TRACKS:
			# [(200, 220), (460, 280), (600, 220), (600, 150), (200, 150), (200, 220)],
			# [(100, 320), (450, 370), (700, 320), (700, 50), (100, 50), (100, 320)])
			# TEMP TRACKS:
			inner,
			[(12, 36), (534, 37), (541, 420), (13, 416), (12, 36)])
		
		# Add the vehicles.
		self.vehicles = SimVehicleManager(self)
		self.vehicles.addVehicle(
			SimVehicle([200,70], 0, 7,
				ngc.ControlSystem(),
				ngc.WallFollowingGuidanceSystem(self,
					wallDistance = 20,
					lookahead = 25),
				color = (1, 0, 0, 0.5)))
		# self.vehicles.addVehicle(
			# SimVehicle([450,120], pi, 6,
				# ngc.ControlSystem(),
				# ngc.PassingGuidanceSystem(self,
					# wallDistance = 12,
					# lookahead = 100),
				# color = (0, 1, 0, 0.5)))
		# self.vehicles.addVehicle(
			# SimVehicle([600,90], pi, 5,
				# ngc.ControlSystem(),
				# ngc.WallFollowingGuidanceSystem(self,
					# lookahead = 20),
				# color = (0, 1, 0, 1)))
		# self.vehicles.addVehicle(
			# SimVehicle([600,60], pi, 5,
				# ngc.ControlSystem(),
				# ngc.WallFollowingGuidanceSystem(self,
					# lookahead = 100),
				# color = (0, 0, 1, 1)))

	def restart(self, obj):
		for vehicle in self.vehicles:
			vehicle.reset()
			self.display.traj[vehicle] = None
	
	def step(self, dt):
		self.display.on_step(self.vehicles)

		for vehicle in self.vehicles:
			# Move the vehicle.
			vehicle.position[0] += cos(vehicle.heading) * vehicle.actualSpeed
			vehicle.position[1] += sin(vehicle.heading) * vehicle.actualSpeed
			
			# Determine guidance.
			desiredHeading = vehicle.guidance.getDesiredHeading(vehicle.position)
			desiredSpeed = vehicle.guidance.getDesiredSpeed(vehicle.position)
			
			# Clamp headings between 0 and 2 * PI.
			vehicle.heading = vehicle.heading % (2 * pi)
			desiredHeading = desiredHeading % (2 * pi)
			
			# Run control algorithm.
			deltaHeading = vehicle.control.heading(vehicle.heading, desiredHeading)
			deltaSpeed = vehicle.control.throttle(vehicle.actualSpeed, desiredSpeed)
			
			# Add some error.
			if randint(0, 5) == 0:
				deltaHeading = deltaHeading + 4 * (random() - 0.5)
			
			# Apply changes to vehicle.
			vehicle.updateHeading(deltaHeading)
			vehicle.updateSpeed(deltaSpeed)
			
			# info = "DESIRED: " + str(degrees(desiredHeading)) + ", ACTUAL: " + str(degrees(vehicle.heading)) + ", DELTA: " + str(degrees(deltaHeading))
			# print(info)
			# Check for a wall collission.
			if not vehicle.guidance.isPointOnTrack(vehicle.position):
				vehicle.actualSpeed = 0
						
		return True #false to stop

if __name__ == '__main__':
	ControlSim().run()