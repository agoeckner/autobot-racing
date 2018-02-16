from random import random
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


class SimDisplay(Widget):
	def __init__(self, **kwargs):
		Color(1, 1, 1, 1, mode='rgba')
		super(SimDisplay, self).__init__(**kwargs)
		
		# Create the trajectory line.
		color = (1, 0, 0, 1)
		with self.canvas:
			Color(*color, mode='rgba')
			d = 30.
			Ellipse(pos=(50 - d / 2, 50 - d / 2), size=(d, d))
			print("Added elipse")
			self.trajectory = Line(points=(0, 0))
	
	def on_touch_down(self, touch):
		color = (0.5, 1, 1)
		with self.canvas:
			Color(*color, mode='hsv')
			d = 30.
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
		print(str(touch.x) + "   " + str(touch.y))
		print(self.to_widget(touch.x, touch.y, False))
	
	def on_step(self, pos):
		if pos == None:
			pos = self.center
	
		self.trajectory.points += pos
		print("Current trajectory: " + str(self.trajectory.points))
		
		color = (0.5, 1, 1)
		with self.canvas:
			Color(*color, mode='hsv')
			d = 30.
			Ellipse(pos=(pos[0] - d / 2, pos[1] - d / 2), size=(d, d))

			
class SimVehicle:
	def __init__(self, initialPosition):
		self.position = initialPosition

class ControlSim(App):

	def build(self):
		# Set up UI.
		parent = Widget()
		self.display = SimDisplay()
		restartBtn = Button(text='Restart')
		restartBtn.bind(on_release=self.restart)
		parent.add_widget(self.display)
		parent.add_widget(restartBtn)
		
		# Set up control system.
		# print("CENTER: " + str(self.display.canvas.center))
		self.control = ControlSystem()
		
		# Add the vehicle.
		self.vehicles = [SimVehicle([250,250])]
		
		# Set up event loop.
		Clock.schedule_interval(self.step, 1)
		
		return parent

	def restart(self, obj):
		self.display.canvas.clear()
		raise Exception("not implemented")
	
	def step(self, dt):
		# print("CENTER: " + str(self.display.to_widget(*self.display.center)))
		print("POS: " + str(self.display.pos))
		print("SIZE: " + str(self.display.size))
		self.vehicles[0].position[0] += 10
		self.vehicles[0].position[1] += 10.5
		self.display.on_step(self.vehicles[0].position)
		return True #false to stop

if __name__ == '__main__':
	ControlSim().run()