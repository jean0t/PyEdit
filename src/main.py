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
