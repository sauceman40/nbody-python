import numpy as np
from utils import typecheck


"""
	A class to keep track of a single particle's state for an N-Body simulation.
"""
class Particle:
	def __init__(self, m, x0, y0, vx0, vy0):
		"""
			Constructor Method.

			Params:
				m:   float -- mass of the particle.
				x0:  float -- initial x position of the particle.
				y0:  float -- initial y position of the particle.
				vx0: float -- initial x velocity of the particle.
				vy0: float -- initial y velocity of the particle.
		"""
		typecheck([m, x0, y0, vx0, vy0], [float, float, float, float, float])
		try:
			assert m > 0.0
		except:
			raise ValueError("m must be greater than zero")

		self.m = m
		self.r = m
		self.x = x0
		self.y = y0
		self.vx = vx0
		self.vy = vy0

	def update_pos(self, h):
		"""
			Update the position of the particle given its current velocity.
			Used with copies of particles for computing forces on each particle.
			update() is used to update the position of each particle when an actual
			step is taken by the system.

			Params:
				h: float -- timestep to be used in approximating the particle's
					next position.
		"""
		typecheck([h], [float])
		try:
			assert h >= 0.0
		except:
			raise ValueError("h must be non-negative")
		self.x += h * self.vx
		self.y += h * self.vy

	def update(self, dvx, dvy, h):
		"""
			Update the position of the particle given an input acceleration and timestep.
			Used to update the position of each particle when an actual
			step is taken by the system.

			Params:
				h:   float -- timestep to be used in approximating the particle's
						next position.
				dvx: float -- particle's x acceleration vector for a given timestep
				dvy: float -- particle's y acceleration vector for a given timestep

		"""

		typecheck([dvx, dvy, h], [float, float, float])
		try:
			assert h >= 0.0
		except:
			raise ValueError("h must be non-negative")
		self.x += h * self.vx
		self.y += h * self.vy
		self.vx += h * dvx
		self.vy += h * dvy

	def dist(self, p2):
		"""
			Compute the distance between the calling particle and another one.

			Params:
				p2: Particle -- The particle you're computing the distance to.

			Returns:
				distance: float -- the distance between this and the input Particle.
		"""
		typecheck([p2], [Particle])
		return np.sqrt((self.x - p2.x)**2 + (self.y - p2.y)**2)

	def copy(self):
		return Particle(self.m, self.x, self.y, self.vx, self.vy)
