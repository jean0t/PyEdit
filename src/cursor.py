class Cursor:
	# It should make the user move around the content
	# It should work properly if used the keys to move around
	# Otherwise I can't guarantee if it will work well
	# but can be mdified with some time and adaptations in the code
	def __init__(self, row=0, column=0, column_hint=None):
		self.row = row
		self.column = column
		self.column_hint = column if column_hint is None else column_hint

	@property
	def column(self):
		return self._column

	@column.setter
	def column(self, column):
		self._column = column
		self._column_hint = column

	def up(self, buffer):
		if self.row > 0:
			self.row -= 1
			self._clamp_col(buffer)

	def down(self, buffer):
		if self.row < len(buffer) - 1:
			self.row += 1
			self._clamp_col(buffer)

	def left(self, buffer):
		if self.column > 0:
			self.column -= 1
		elif self.row > 0:
			self.row -= 1
			self.column = len(buffer[self.row])

	def right(self, buffer):
		if self.column < len(buffer[self.row]):
			self.column += 1

		elif self.row < len(buffer) - 1:
			self.row += 1
			self.column = 0

	def _clamp_col(self, buffer):
		self.column = min(self._column_hint, len(buffer[self.row]))
