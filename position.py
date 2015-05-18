class Position():
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __hash__(self):
		return hash((self.row(), self.column()))
		
	def __eq__(self, other):
		return isinstance(other, self.__class__) \
			and self.__dict__ == other.__dict__

	def __ne__(self, other):
		return not self.__eq__(other)

	def as_tuple(self):
		return (self.row(), self.column())

	def row(self):
		return self.x

	def column(self):
		return self.y