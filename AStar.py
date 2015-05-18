from environment import Environment
from position import Position
from actor import Actor
from time import sleep

size = 10
wall_chance = 6
environment = Environment(size, size, wall_chance)

start = Position(size - 1, 0)
end = Position(0, size - 1)

actor = Actor(start, environment)
environment.actor_add(actor)

# DEBUG
# Single corridor
"""for i in xrange(0, size):
	if ((i, 0) in environment.obstacles) and i < size - 1:
		del environment.obstacles[(i, 0)]
	if ((0, i) in environment.obstacles):
		del environment.obstacles[(0, i)]
	environment.obstacles[(1, i)] = '#'
	environment.obstacles[(i, 1)] = '#'
environment.print_state()"""

# All clear
environment.obstacles = {}

# Double walls
d = 3
for i in xrange(d, size):
	environment.obstacles[(5, i)] = '#'
	environment.obstacles[(7, i - d)] = '#'
# + Extra wall
for i in xrange(0, 4):
	environment.obstacles[(i, 6)] = '#'

# Diagonal wall
"""d = 5
for i in xrange(d, size):
	environment.obstacles[(i, i - d)] = '#'
del environment.obstacles[(7, 2)]"""

# Specific points
"""environment.obstacles[(9, 4)] = '#'
environment.obstacles[(8, 6)] = '#'"""
# DEBUG

#print "\n"*100

actor.move(end)
actor.act()

for i in actor.actions:
	print i.position.as_tuple()

environment.print_state()

while actor.can_act():
	sleep(0.25)
	a = actor.act()
	actor.state = a
	print '\n'*100
	print a.as_tuple()
	environment.print_state()
	if not actor.can_act():
		break