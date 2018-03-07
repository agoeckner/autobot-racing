from random import randint, random
from math import *
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line

# Import control/guidance modules from the actual program.
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], "..", "autobot-racing"))
from controls.Controls import *

Window.clearcolor = (1, 1, 1, 1)

class SimDisplay(Widget):
	FUTURE_LINE_SCALE = 100

	def __init__(self, track, **kwargs):
		super(SimDisplay, self).__init__(**kwargs)
		
		self.track = track
		self.traj = {}
	
	def on_step(self, vehicles):
		# Reset canvas.
		self.canvas.clear()
		
		# Display the track.
		color = (0, 0, 0, 1)
		with self.canvas:
			Color(*color, mode='rgba')
			self.innerWall = Line(points=self.track.innerWall, width=2.0)
			self.outerWall = Line(points=self.track.outerWall, width=3.0)
		
		# Trajectory lines.
		for vehicle in vehicles:
			pos = vehicle.position
			futurePoint = (pos[0] + cos(vehicle.heading) * vehicle.speed * self.FUTURE_LINE_SCALE,
				pos[1] + sin(vehicle.heading) * vehicle.speed * self.FUTURE_LINE_SCALE)
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
				d = 5.
				Ellipse(pos=(pos[0] - d / 2, pos[1] - d / 2), size=(d, d), width=5)

class SimTrack:
	def __init__(self, innerWall, outerWall):
		self.innerWall = innerWall
		self.outerWall = outerWall
			
class SimVehicle:
	MIN_TURN_ANGLE = pi / 24

	def __init__(self, initialPosition, initialHeading, initialSpeed,
			control, guidance, color = (1, 0, 0, 1)):
		self.initialPosition = initialPosition
		self.initialHeading = initialHeading
		self.initialSpeed = initialSpeed
		self.position = initialPosition
		self.heading = initialHeading
		self.speed = initialSpeed
		self.color = color
		self.control = control
		self.guidance = guidance
	
	def reset(self):
		self.position = self.initialPosition
		self.heading = self.initialHeading
		self.speed = self.initialSpeed
	
	def updateHeading(self, delta):
		# Clamp the turn rate.
		if delta > 0:
			self.heading += min(delta, self.MIN_TURN_ANGLE)
		else:
			self.heading += max(delta, -self.MIN_TURN_ANGLE)
		
		# Clamp the heading.
		self.heading = self.heading % (2 * pi)
	
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
		Clock.schedule_interval(self.step, 1 / 20)
		
		return parent
	
	def initSim(self):
		# Add the track.
		self.track = SimTrack(
			[(200, 220), (460, 280), (600, 220), (600, 150), (200, 150), (200, 220)],
			[(100, 320), (450, 370), (700, 320), (700, 50), (100, 50), (100, 320)])
		
		# Add the vehicles.
		self.vehicles = [
			SimVehicle([600,120], pi, 7,
				ControlSystem(),
				WallFollowingGuidanceSystem(self.track,
					wallDistance = 10,
					lookahead = 200),
				color = (1, 0, 0, 1)),
			SimVehicle([600,90], pi, 5,
				ControlSystem(),
				WallFollowingGuidanceSystem(self.track,
					lookahead = 20),
				color = (0, 1, 0, 1)),
			SimVehicle([600,60], pi, 5,
				ControlSystem(),
				WallFollowingGuidanceSystem(self.track,
					lookahead = 100),
				color = (0, 0, 1, 1)),
		]

	def restart(self, obj):
		for vehicle in self.vehicles:
			self.display.traj[vehicle] = None
			vehicle.reset()
	
	def step(self, dt):
		self.display.on_step(self.vehicles)
		# return
		for vehicle in self.vehicles:
			# Move the vehicle.
			vehicle.position[0] += cos(vehicle.heading) * vehicle.speed
			vehicle.position[1] += sin(vehicle.heading) * vehicle.speed
			
			# Determine guidance.
			desiredHeading = vehicle.guidance.getDesiredHeading(vehicle.position)
			desiredSpeed = vehicle.guidance.getDesiredSpeed(vehicle.position)
			
			# Run control algorithm.
			deltaHeading = vehicle.control.heading(vehicle.heading, desiredHeading)
			deltaSpeed = vehicle.control.throttle(vehicle.speed, desiredSpeed)
			
			# Add some error.
			if randint(0, 5) == 5:
				deltaHeading = deltaHeading + 50 * (random() - 0.5)
			
			# Apply changes to vehicle.
			vehicle.updateHeading(deltaHeading)
			vehicle.updateSpeed(deltaSpeed)
			
			# Check for a wall collission.
			if not vehicle.guidance.isPointOnTrack(vehicle.position):
				vehicle.speed = 0
			
		return True #false to stop

if __name__ == '__main__':
	ControlSim().run()