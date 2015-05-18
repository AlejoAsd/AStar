def none(state):
	return 0

def manhattan_distance(state):
	return abs(state.target.x - state.position.x) + abs(state.target.y - state.position.y)