import csv
from queue import PriorityQueue
from itertools import count
# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
	grid = []
	with open(filepath, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			grid.append(row)
	m, n = len(grid), len(grid[0])

	start = None
	goals = []
	treasures = []
	treasureCollected = 0

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
	frontier.put((0, next(counter), 0, start, frozenset() , [start]))
	explored = set()
	numStatesExplored = 0

	def heuristic(pos):
		if not goals: return 0
		if treasureCollected >= 5: return closestGoalDistance(pos)
		return closestTreasureDistance(pos)

	def closestTreasureDistance(pos):
		treasureDistances = {t:manh(pos, t) for t in treasures}
		minDist = min(treasureDistances.values())
		minDistTreasures = [k for k, v in treasureDistances.items() if v == minDist]

		return min(closestGoalDistance(t) for t in minDistTreasures)

	def closestGoalDistance(pos):
		return min(manh(pos, g) for g in goals)

	def manh(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
		
	# optimal_path is a list of coordinate of squares visited (in order)
	# optimal_path_cost is the cost of the optimal path
	# num_states_explored is the number of states explored during A* search
	
	# return optimal_path, optimal_path_cost, num_states_explored