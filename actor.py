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
	position = None
	target = None
	parent = None
	cost = 0

	def __init__(self, position, target, cost=0, parent=None):
		self.position = position
		self.target = target
		self.parent = parent

		# F(n)
		self.cost = cost

	def __str__(self):
		return str(self.as_tuple())

	def __hash__(self):
		return hash((self.position, self.target))
		#return hash((hash(self.position), hash(self.target)))

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

	def frontier_order(self, state):
		return -state.cost

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

			# Create chain of actions
			if (result):
				s = result.parent
				
				while s is not None:

					self.actions.append(s)
					s = s.parent

				result = True

		if (result):
			return self.actions.pop()
		else:
			print "No solution found"
			return None

	def think(self, state):
		if state.goal():
			self.actions.append(state)
			return state

		s = state.as_tuple()

		# Add to current state to explored
		self.explored.add(s)

		# Expand frontier
		self.expand_frontier(state, s[ROW] + 1, s[COLUMN])
		self.expand_frontier(state, s[ROW] - 1, s[COLUMN])
		self.expand_frontier(state, s[ROW], s[COLUMN] + 1)
		self.expand_frontier(state, s[ROW], s[COLUMN] - 1)

		# Keep thinking
		try:
			n = self.frontier.pop()
			return self.think(n)
		except:
			return None

	def expand_frontier(self, state, row, col):
		# Get the new position
		position = Position(row, col)
		# Rule out invalid positions
		if position.row() < 0 or position.column() < 0 or \
		   position.row() >= self.environment.height or position.column() >= self.environment.width:
			return

		p = position.as_tuple()

		# If not a wall and not explored, then add to frontier
		if p not in self.environment.obstacles and p not in self.explored:
			new_state = State(position, state.target, state.cost + 1, state)

			# Calculate cost
			cost = new_state.cost + 2 * self.heuristic(new_state)
			print cost

			# Add to frontier
			self.frontier.add(new_state)
			self.explored.add(new_state)