#!/usr/bin/python
import math
import numpy as np
import random
from particle import Particle
from utils import typecheck




class NBodySimulator:

	def __init__(self, N=30, speed=1.0):


		# Validate variables
		typecheck([N, speed], [int, float])
		try:
			assert N > 1
		except:
			raise ValueError("N (# of particles) must be greater than one")
		try:
			assert speed >= 0.0
		except:
			raise ValueError("speed must be non-negative")

		self.N = N
		self.h = 0.005 * speed # Choose a small h, proportional to input speed
		self.a = 0.2 # a should be small as well, such that a^2 < 0.1
		self.bounds = [-1., 1., -1., 1.] # bounding box of the simulation

		# Create N Particles, store in internal array
		self.particles = []
		for i in range(N):
			# For each particle, initialize mass randomly between 1 and 10 units,
			# and a small initial position and velocity
			m = 1.0#random.uniform(1.0, 10.0)
			x0, y0 = 2., 2.
			vx0, vy0 = 1., 1.
			while x0**2 + y0**2 > 1:
				x0, y0 = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
			alpha = random.uniform(0, 2*np.pi)
			vx0 = np.sqrt(0.1) * np.cos(alpha)
			vy0 = np.sqrt(0.1) * np.sin(alpha)
			self.particles.append(Particle(m, x0, y0, vx0, vy0))


	def gforce(self, p1, p2):
		typecheck([p1, p2], [Particle, Particle])
		dx = p1.x - p2.x
		dy = p1.y - p2.y
		r = p1.dist(p2)
		f = - p1.m * p2.m / (r**2 + self.a**2)
		#return [f*dx/r, f*dy/r]  --- Small r does weird things here. So we approximate it as 1.
		return [f*dx, f*dy]


	def take_step(self):
		updates = []
		# Calculate updates for each particle -- use Symplectic Integration
		for i in range(self.N):
			p1 = self.particles[i]
			p = p1
			ax = 0
			ay = 0
			ptemp = p1.copy()
			ptemp.update_pos(self.h)
			for j in range(i) + range(i+1, self.N):
				p2 = self.particles[j]
				# Gravitational forces
				axj, ayj = self.gforce(ptemp, p2)
				ax += axj / ptemp.m
				ay += ayj / ptemp.m

				#TODO: Collision forces between particles



			updates.append([ax, ay])

		#TODO: Collision forces with the bounding box

		# Apply each update to the corresponding particle
		for i in range(self.N):
			p1 = self.particles[i]
			u = updates[i]
			p1.update(u[0], u[1], self.h)
			self.particles[i] = p1





	def getParticleLocations(self):
		xVals = [self.particles[i].x for i in range(self.N)]
		yVals = [self.particles[i].y for i in range(self.N)]
		return [xVals, yVals]


	def getParticleMasses(self):
		return np.array([self.particles[i].m for i in range(self.N)])

	def getParticleRadii(self):
		return np.array([self.particles[i].r for i in range(self.N)])
