# Name this file to assignment1.py when you submit
import csv
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

	for r in range(m):
		for c in range(n):
			tempValue = grid[r][c]
			if tempValue == 'S':
				start = (r, c) # stores as (x, y)
			elif tempValue == 'G':
				goals.append((r,c)) # stores as (x, y) in goals list
			elif val.isdigit() and int(tempValue) > 0:
				treasures.append((r,c, int(tempValue))) # stores as (x, y value) in treasures list

	# optimal_path is a list of coordinate of squares visited (in order)
	# optimal_path_cost is the cost of the optimal path
	# num_states_explored is the number of states explored during A* search
	return optimal_path, optimal_path_cost, num_states_explored

def distance(r1, r2, c1, c2): # Manhattan Distance
	return (r2 - r1) + (c2 - c1)

def calculateHeuristic(row, col, curTrsrVal):
	# reqTrsrVal = 5 - curTrsrVal
	pass
