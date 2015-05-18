from random import random
from math import floor
from position import Position
from actor import Actor

class Environment():
	# CONSTANTS
	CLEAR = ' '
	ACTOR = 'O'
	WALL = '#'

	obstacles = {}
	height = 0
	width = 0
	wall_chance = 0

	actors = []

	def __init__(self, height, width, wall_chance):
		self.height = height
		self.width = width
		self.wall_chance = wall_chance

		self.initialize()

	def initialize(self):
		for row in xrange(0, self.height):
			for col in xrange(0, self.width):
				rand = floor(random() * self.wall_chance)
				if rand == 0:
					self.obstacles[(row, col)] = self.WALL
		if (0, self.width - 1) in self.obstacles:
			del self.obstacles[(0, self.width - 1)]
		if (self.height - 1, 0) in self.obstacles:
			del self.obstacles[(self.height - 1, 0)]

	def actor_add(self, actor):
		self.actors.append(actor)

	def actor_remove(self, actor):
		self.actors.remove(actor)

	def print_state(self):
		for row in xrange(0, self.height):
			for col in xrange(0, self.width):
				s = self.CLEAR

				p = (row, col)
				# Actor
				for actor in self.actors:
					if p == actor.state.as_tuple():
						s = self.ACTOR
				# Obstacles
				if p in self.obstacles:
					obstacle = self.obstacles[p]
					# Wall
					if obstacle == self.WALL:
						s = self.WALL						

				print s,
			print ''