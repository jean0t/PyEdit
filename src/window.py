class Window: # It exists to provide a screen dinamically
	# Last time it was crashing by not having enough space lol
	# it solves the problem
	def __init__(self, n_rows, n_columns):
		self.n_rows = n_rows
		self.n_columns = n_columns
