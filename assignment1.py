# Name this file to assignment1.py when you submit
import csv
from queue import PriorityQueue
from itertools import count
# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
	# filepath is the path to a CSV file containing a grid
	grid = []
	with open(filepath, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			grid.append(row)
	m, n = len(grid), len(grid[0])

	start = None
	goals = []
	treasures = []

	for row in range(m):
		for col in range(n):
			tempValue = grid[row][col]
			if tempValue == 'S':
				start = (row, col) # stores as (x, y)
			elif tempValue == 'G':
				goals.append((row, col)) # stores as (x, y) in goals list
			elif tempValue.isdigit() and int(tempValue) > 0:
				treasures.append((row, col, int(tempValue))) # stores as (x, y value) in treasures list
	
	frontier = PriorityQueue()
	counter = count()
	frontier.put((0, next(counter), 0, start, , [start]))
	explored = set()
	numStatesExplored = 0

	def heuristic(pos, collected)
		row , col = pos
		if goals:
			return min(abs(row - goalRow) + abs(col - goalCol) for (goalRow, goalCol) in goals)
		return 0

	while not frontier.empty():
		
	# optimal_path is a list of coordinate of squares visited (in order)
	# optimal_path_cost is the cost of the optimal path
	# num_states_explored is the number of states explored during A* search
	
	# return optimal_path, optimal_path_cost, num_states_explored