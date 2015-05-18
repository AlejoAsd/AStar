from random import random
from math import floor
from position import Position
from actor import Actor

class Environment():
	# CONSTANTS
	CLEAR = ' '
	ACTOR = 'O'
	GOAL = 'X'
	WALL = '#'

	# INITIALIZATION TYPE
	EMPTY = 0
	WALLS = 1
	RANDOM = 2

	obstacles = None
	height = 0
	width = 0

	actors = []

	def __init__(self, height, width, initialization_type, *initialization_args):
		self.height = height
		self.width = width

		self.obstacles = {}
		self.initialize(initialization_type, *initialization_args)

	def initialize(self, initialization_type, *initialization_args):
		if initialization_type == self.EMPTY:
			return
		elif initialization_type == self.WALLS:
			self.create_walls(*initialization_args)
		elif initialization_type == self.RANDOM:
			self.create_random_obstacles(*initialization_args)

	def create_walls(self, *initialization_args):
		for row in xrange(0, self.height):
			self.obstacles[(row, 0)] = self.WALL
			self.obstacles[(row, self.width - 1)] = self.WALL
			if row == 0 or row == (self.height - 1):
				for col in xrange(1, self.width):
					self.obstacles[(row, col)] = self.WALL

	def create_random_obstacles(self, *initialization_args):
		"""Creates random walls in a 1/WALL_CHANCE chance. Zero means no walls, but you may want to use a CLEAR initialization for that."""
		WALL_CHANCE = 0
		for row in xrange(0, self.height):
			for col in xrange(0, self.width):
				rand = floor(random() * initialization_args[WALL_CHANCE])
				if rand == 0:
					self.obstacles[(row, col)] = self.WALL

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
					if p == actor.state.position.as_tuple():
						s = self.ACTOR
					elif p == actor.state.target.as_tuple():
						s = self.GOAL
					elif p in actor.explored:
						s = 'V'
				# Obstacles
				if p in self.obstacles:
					obstacle = self.obstacles[p]
					# Wall
					if obstacle == self.WALL:
						s = self.WALL						

				print s,
			print ''