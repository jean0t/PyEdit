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

# importing external classes
from src.cursor import Cursor
from src.window import Window
from src.main import main # this will make the software actually run



if __name__ == '__main__':
	curses.wrapper(main) # calls the function and shows exceptions without messing with the terminal
