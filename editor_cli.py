#!/usr/bin/env python3

import curses, sys, argparse

class Cursor:
	def __init__(self, row=0, column=0):
		self.row = row
		self.column = column

	def up(self):
		self.row -= 1
	
	def down(self):
		self.row += 1
	
	def left(self):
		self.column -= 1
	
	def right(self):
		self.column += 1

class Window:
	def __init__(self, n_rows, n_columns):
		self.n_rows = n_rows
		self.n_columns = n_columns

def main(stdscr):
	parser = argparse.ArgumentParser()
	parser.add_argument("filename")
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

		key = stdscr.getkey()
		if key == 'q':
			sys.exit(0)

		elif key == 'KEY_UP':
			cursor.up()

		elif key == 'KEY_DOWN':
			cursor.down()
		
		elif key == 'KEY_LEFT':
			cursor.left()

		elif key == 'KEY_RIGHT':
			cursor.right()

if __name__ == '__main__':
	curses.wrapper(main)
