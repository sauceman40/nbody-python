import Tkinter as tk
from animator import NBodyAnimator
import sys

class NBodyGUI(tk.Tk):
	def __init__(self, parent):
		tk.Tk.__init__(self, parent)
		self.parent = parent

		# Init parameters
		self.selectedSpeed = 0.5
		self.nParticles = 50
		self.speedMap = {
			"Slow": 0.5,
			"Medium": 0.8,
			"Fast": 2.0,
			"Extreme": 4.0
		}

		# Init UI
		self.grid()
		self.speedLabel = tk.Label(self, text="Particle Speed:")
		self.speedLabel.grid(column=0, row=0, padx=50, pady=(10, 0))
		self.variable = tk.StringVar(self)
		self.variable.set("Slow")
		self.speedBox = tk.OptionMenu(self, self.variable,
						  "Slow", "Medium", "Fast", "Extreme",
						  command = self.speedMenu)
		self.speedBox.grid(column=0, row=1, sticky="nsew", padx=50, pady=(0, 25))

		self.sliderLabel = tk.Label(self, text="# Particles:")
		self.sliderLabel.grid(column=0, row=2, padx=20, pady=(0, 0))
		self.particleSlider = tk.Scale(self, from_=30, to=75, orient=tk.HORIZONTAL, \
			command=self.setNumParticles)
		self.particleSlider.grid(column=0, row=3, padx=50, pady=(0, 25))

		self.button = tk.Button(self, text="Simulate",\
			command=self.runSimulation)
		self.button.grid(column=0, row=4, padx=50, pady=(0, 10))

	def runSimulation(self):
		if self.selectedSpeed > 0:
			self.animator = NBodyAnimator(numpoints=self.nParticles, speed=self.selectedSpeed)
			self.animator.show()

	def speedMenu(self, selection):
		self.selectedSpeed = self.speedMap[selection]

	def setNumParticles(self, selection):
		self.nParticles = self.particleSlider.get()
