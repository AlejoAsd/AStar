from position import Position
from heuristic import none, manhattan_distance
from copy import copy, deepcopy
from sortedcontainers.sortedset import SortedSet

# Tuple values
ROW = 0
COLUMN = 1

# Item constants
KEY = 0
VALUE = 1

# Frontier entries
COST = 0
STATE = 1

class State():
	# SENSOR CONSTANTS
	BUMPED = 0
	POSITION_X = 1
	POSITION_Y = 2

	position = None
	target = None
	parent = None

	cost = 0
	path_cost = None

	def __init__(self, position, target, cost=0, parent=None):
		self.position = position
		self.target = target
		self.parent = parent

		# G(n)
		self.cost = cost

	def __str__(self):
		return str(self.as_tuple())

	def __hash__(self):
		return hash((self.position, self.target))

	def __eq__(self, other):
		return isinstance(other, self.__class__) \
			and self.position == other.position \
			and self.target == other.target

	def __ne__(self, other):
		return not self.__eq__(other)

	def __lt__(self, other):
		return self.cost < other.cost

	def as_tuple(self):
		return (self.row(), self.column())

	def row(self):
		return self.position.row()

	def column(self):
		return self.position.column()

	def goal(self):
		return self.position.as_tuple() == self.target.as_tuple()

class Actor():
	state = None
	environment = None
	heuristic = None

	frontier = None
	explored = None

	c = 0
	f = 0

	actions = []

	def __init__(self, position, environment):
		self.state = State(position, position)
		self.environment = environment
		self.heuristic = manhattan_distance

		self.frontier = SortedSet(key = self.frontier_order)
		self.explored = set()

		self.reset()

	def update(self, action):
		self.state = action
		self.state.parent = None

	def move(self, position):
		self.state.target = position

	def can_act(self):
		return len(self.actions)

	def reset(self):
		self.actions = []
		self.frontier.clear()
		self.explored.clear()
		self.explored.add(self.state)
		self.c = 0
		self.f = 0

	def frontier_order(self, state):
		return -state.path_cost

	def act(self):
		# Recalculate when bumping
		#if sensors[BUMPED] == 1:
		#	del self.actions

		# No action is needed if we are at the target
		if self.state.goal():
			return None

		result = True
		if not self.can_act():
			# Reset values
			self.reset()

			# Think
			result = self.think(self.state)

		# If a route is already calculated, return next action
		if (result):
			return self.actions.pop()
		else:
			print "No solution found"
			return None

	def think(self, state):
		# Define the initial frontier
		self.expand_frontier(state)

		frontier_size = 1
		while frontier_size:
			self.c += 1

			# Get lowest valued frontier state
			state = self.frontier.pop()

			# Check for goal
			if state.goal(): 
				self.recreate_actions(state)
				return True

			# Add current state to explored
			self.explored.add(state.as_tuple())

			# Expand frontier
			self.expand_frontier(state)

			frontier_size = len(self.frontier)

			# DEBUG
			"""s = ''
			for i in self.frontier:
				s += "{}:({},{}) ".format(i.cost, i.row(), i.column())
			print s"""
			# DEBUG
		return False

	def expand_frontier(self, state):
		for row in (-1, 0, 1):
			for col in (-1, 0, 1):
				# Only allow adjacent non-diagonal moves
				#if row != 0 and col != 0:
				#	continue

				# Get the new position
				position = Position(state.row() + row, state.column() + col)

				# Rule out invalid positions
				if position.row() < 0 or position.column() < 0 or \
				   position.row() >= self.environment.height or position.column() >= self.environment.width:
					return

				p = position.as_tuple()

				# If not an obstacle and not explored, then add to frontier
				if p not in self.environment.obstacles and p not in self.explored:
					self.f += 1

					# Create the new state
					new_state = State(position, state.target, state.cost + 1, state)

					# Update state path cost
					new_state.path_cost = new_state.cost + self.heuristic(new_state)
					

					# Add to frontier
					self.frontier.add(new_state)

	def recreate_actions(self, state):
		while state is not None:
			self.actions.append(state)
			state = state.parent