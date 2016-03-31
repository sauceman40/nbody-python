#!/usr/bin/python
import math
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import Tkinter as tk
from simulator import NBodySimulator
from utils import typecheck

class NBodyAnimator(object):
	"""A utility class to animate a scatter plot using matplotlib.animations.FuncAnimation."""
	def __init__(self, numpoints=50, speed=0.3):

		typecheck([numpoints, speed], [int, float])
		try:
			assert speed >= 0.0
		except:
			raise ValueError("speed must be non-negative")
		try:
			assert numpoints > 1
		except:
			raise ValueError("N (# of particles) must be greater than one")

		# Set up internal members
		self.numpoints = numpoints
		self.speed = speed
		self.pause = False
		self.stop = False
		self.stream = self.data_stream()

		# Set up visualizations
		self.fig = plt.figure()
		self.fig.set_dpi(100)
		self.fig.set_size_inches(5, 5)

		self.ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
		patches = plt.Circle((5, -5), 0.75, fc='y')


		self.ani = animation.FuncAnimation(self.fig, self.update, interval=5,
										   init_func=self.setup_plot, blit=True)
		self.fig.canvas.mpl_connect('button_press_event', self.togglePlay)
		self.fig.canvas.mpl_connect('key_press_event', self.closeWindow)


	def setup_plot(self):
		"""Draws the initial state of the scatter plot."""
		x, y, s, c = next(self.stream)
		self.scat = self.ax.scatter(x, y, c=c, s=s, animated=True)
		self.ax.axis([-1.0, 1.0, -1.0, 1.0])

		# For FuncAnimation's sake, we need to return the artist we'll be using
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,


	def data_stream(self):
		"""Return an endless data stream for receiving each iterative state of the scatter plot"""
		nbs = NBodySimulator(N=self.numpoints, speed=self.speed)

		# Reshape data from each iteration into a format readable by FuncAnimation
		data = nbs.getParticleLocations()
		data.append(nbs.getParticleRadii())
		data.append(np.random.rand(self.numpoints))
		data = np.array(data)
		while not self.stop:
			if not self.pause:
				nbs.take_step()
				data[:2] = nbs.getParticleLocations()
			yield data

	def update(self, i):
		"""Utility function called internally to update the scatter plot."""
		data = next(self.stream)

		# Set x and y data...
		self.scat.set_offsets(data[:2, :])
		# Set sizes...
		self.scat._sizes = data[2]
		# Set colors..
		self.scat.set_array(data[3])

		# Return next state of Scatter Plot for FuncAnimation to draw..
		return self.scat,


	def show(self):
		"""Show the scatter plot in a new window."""
		plt.show()

	def togglePlay(self, event):
		self.pause ^= True

	def closeWindow(self, event):
		if event.key in ['x', 'q']:
			if not self.pause:
				self.togglePlay(event)
			self.stop = True
			self.ani._stop()
			plt.close(self.fig)
