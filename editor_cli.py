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

class Window: # It exists to provide a screen dinamically
	# Last time it was crashing by not having enough space lol
	# it solves the problem
	def __init__(self, n_rows, n_columns):
		self.n_rows = n_rows
		self.n_columns = n_columns

def main(stdscr):
	parser = argparse.ArgumentParser()
	parser.add_argument("filename") # no argument means empty
	args = parser.parse_args()

	with open(args.filename) as f:
		buffer = f.readlines()
	
	window = Window(curses.LINES - 1, curses.COLS - 1)
	cursor = Cursor()
	while True:
		stdscr.erase()
		for row, line in enumerate(buffer[:window.n_rows]):
			stdscr.addstr(row, 0, line[:window.n_columns])
		stdscr.move(cursor.row, cursor.column)

		key = stdscr.getkey() # self explanatory but
		# it will be the menu to add functionality based
		# on the key press
		if key == 'q':
			sys.exit(0)

		elif key == 'KEY_UP':
			cursor.up(buffer)

		elif key == 'KEY_DOWN':
			cursor.down(buffer)
		
		elif key == 'KEY_LEFT':
			cursor.left(buffer)

		elif key == 'KEY_RIGHT':
			cursor.right(buffer)

if __name__ == '__main__':
	curses.wrapper(main) # calls the function and shows exceptions
	# without messing with the terminal
