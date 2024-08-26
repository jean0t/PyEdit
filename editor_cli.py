#!/usr/bin/env python3

# CLI TEXT EDITOR
# THIS PROJECT IS MADE USING THE CURSES MODULE OF PYTHON
# TO PROVIDE A CLI INTERFACE AND WORK WITH IT
#
# the project will be the implementation of a simple and lightweight
# text editor, simple enough for anyone to change and add functionality
# or modify the code, but keep it open source for others, as GPL3 says so


import curses, sys, argparse 
# curses is the most important
# sys will deal with exits only
# and argparse will deal with files to edit 

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
		if self.row < buffer.bottom: 
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

		elif self.row < buffer.bottom:
			self.row += 1
			self.column = 0

	def _clamp_col(self, buffer):
		self.column = min(self._column_hint, len(buffer[self.row]))

class Window:
	# It exists to provide a screen dinamically
	# Last time it was crashing by not having enough space lol
	# it solves the problem
	def __init__(self, n_rows, n_columns, row=0, column=0):
		self.n_rows = n_rows
		self.n_columns = n_columns
		self.row = row
		self.column = column

	def translate(self, cursor):
		return cursor.row - self.row, cursor.column - self.column

	def horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
		n_pages = cursor.column // (self.n_columns - right_margin)
		self.column = max(n_pages * self.n_columns - right_margin - left_margin, 0)

	@property
	def bottom(self):
		return self.row + self.n_rows - 1

	def up(self, cursor):
		if cursor.row == self.row - 1 and self.row > 0:
			self.row -= 1

	def down(self, buffer, cursor):
		if cursor.row == self.bottom + 1 and self.bottom < buffer.bottom:
			self.row += 1

class Buffer:
	# let's actually modify the text it receives
	# but firstly we actually need that class
	def __init__(self, lines):
		self.lines = lines

	def __len__(self):
		return len(self.lines)

	def __getitem__(self, index):
		return self.lines[index]

	@property
	def bottom(self):
		return len(self) - 1

	def insert(self, cursor, string):
		row, column = cursor.row, cursor.column
		current = self.lines.pop(row)
		new = current[:column] + string + current[column:]
		self.lines.insert(row, new)

	def split(self, cursor):
		row, column = cursor.row, cursor.column
		current = self.lines.pop(row)
		self.lines.insert(row, current[:column])
		self.lines.insert(row + 1, current[column:])

def right(window, buffer, cursor):
	cursor.right(buffer)
	window.down(buffer, cursor)
	window.horizontal_scroll(cursor)


def main(stdscr):
	parser = argparse.ArgumentParser()
	parser.add_argument("filename") # no argument means empty
	args = parser.parse_args()

	with open(args.filename) as f:
		buffer = Buffer(f.read().splitlines())

	window = Window(curses.LINES - 1, curses.COLS - 1)
	cursor = Cursor()
	while True:
		stdscr.erase()
		for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
			if row == cursor.row - window.row and window.column > 0:
				line = '<<' + line[window.column + 1]
			if len(line) > window.n_columns:
				line = line[:window.n_columns - 1] + '>>'
			stdscr.addstr(row, 0, line)

		stdscr.move(*window.translate(cursor))

		key = stdscr.getkey() # self explanatory but
		# it will be the menu to add functionality based
		# on the key press
		if key == chr(0x18) :
			sys.exit(0)

		elif key == 'KEY_UP':
			cursor.up(buffer)
			window.up(cursor)
			window.horizontal_scroll(cursor)

		elif key == 'KEY_DOWN':
			cursor.down(buffer)
			window.down(buffer, cursor)
			window.horizontal_scroll(cursor)

		elif key == 'KEY_LEFT':
			cursor.left(buffer)
			window.up(cursor)
			window.horizontal_scroll(cursor)

		elif key == 'KEY_RIGHT':
			right(window, buffer, cursor)

		elif key == '\n':
			buffer.split(cursor)
			right(window, buffer, cursor)

		else:
			buffer.insert(cursor, key)
			for _ in key:
				right(window, buffer, cursor)

if __name__ == '__main__':
	curses.wrapper(main) # calls the function and shows exceptions
	# without messing with the terminal
