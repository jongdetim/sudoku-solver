import ast
import sys
import numpy as np

class Sudoku:
	def __init__(self, starting_state):
		try:
			self.state = np.array(starting_state, dtype='int8')
		except:
			self.input_invalid()
			exit()

	def	print_state(self):
		print(self.state)

	def done(self):
		print(self.state)
		print('solved!')
		exit()

	def input_invalid(self):
		print('a sudoku is a 9 by 9 array with numbers between 0 and 9')
		return False

	def	valid_input(self):
		if self.state.shape != (9, 9):
			return self.input_invalid()

		for ynum, y in enumerate(self.state):
			for xnum, num in enumerate(y):
				if num > 9 or num < 0 or (num != 0 and not self.check_legal(ynum, xnum, num)):
					return self.input_invalid()

		return True

	def check_legal(self, y, x, num):
		row, column, block = False, False, False

		if num not in self.state[y][np.arange(9) != x]:
			row = True

		if num not in self.state[:, x][np.arange(9) != y]:
			column = True

		mask = np.ones([3, 3], bool)
		mask[y % 3, x % 3] = False
		y -= y % 3
		x -= x % 3
		if num not in self.state[y:y + 3, x:x + 3][mask]:
			block = True

		return row == True & column == True & block == True

	def solve(self, y=0, x=0):
		num = 1
		while self.state[y][x] != 0:
			x += 1
			if x > 8:
				y += 1
				x = 0
				if y > 8:
					self.done()
		
		while num < 10:
			self.state[y][x] = num
			if self.check_legal(y, x, num):
				if x < 8:
					self.solve(y, x + 1)
				elif y < 8:
					self.solve(y + 1, 0)
				else:
					self.done()
			num += 1

		if num == 10:
			self.state[y][x] = 0
			return 0


def main(starting_state):
	game = Sudoku(starting_state)
	if game.valid_input():
		if game.solve() == 0:
			print('sudoku can not be solved')
	else:
		print('input is not valid')

# ______________________EXECUTION_________________________

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print('usage: python sudoku_solver.py path_to_sudoku_file')
		exit()

	filename = sys.argv[1]
	with open(filename, 'r') as sudoku_file:
		sudoku_string = sudoku_file.read()
		try:
			starting_state = ast.literal_eval(sudoku_string)
		except:
			print('input file is not correctly formatted')
			exit()

	main(starting_state)
