def none(state):
	return 0

def manhattan_distance(state):
	return abs(state.target.row() - state.position.row()) + abs(state.target.column() - state.position.column())