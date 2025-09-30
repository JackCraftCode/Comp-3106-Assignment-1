import csv
import heapq


# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath) -> tuple[list[tuple[int, int]], int ,int]:
	grid = []
	start = None
	goals = []
	treasures = []

	with open(filepath, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			grid.append(row)

	r = len(grid)
	c = len(grid[0])

	for row in range(r):
		for col in range(c):
			tempValue = grid[row][col]
			if tempValue == 'S':
				start = (row, col)  # stores as (x, y)
			elif tempValue == 'G':
				goals.append((row, col))  # stores as (x, y) in goals list
			elif tempValue.isdigit() and int(tempValue) > 0:
				treasures.append((row, col, int(tempValue)))  # stores as (x, y, value) in treasures list

	results = aStarSearch(grid, start, goals, treasures)
	return results[0], len(results[0]), results[1]


def aStarSearch(grid: list[list[int]],
                start: tuple[int, int],
                goals: list[tuple[int, int]],
                treasures: list[tuple[int, int, int]]) -> tuple[list[tuple[int, int]] ,int]:
	treasureCollected = 0
	numStatesExplored = 0
	startNode = createNode(
		pos = start,
		g = 0,
		h = heuristic(start, goals, treasures, treasureCollected)
	)

	openList = [(startNode['f'], start)] # Priority queue
	openDict = {start: startNode}        # For quick node lookup
	closedSet = set()                    # Explored nodes

	while openList:
		_, currentPos = heapq.heappop(openList)
		currentNode = openDict[currentPos]

		if currentPos in goals and treasureCollected >= 5:
			return reconstructPath(currentNode), numStatesExplored

		closedSet.add(currentPos)

		for neighborPos in getValidNeighbors(grid, currentPos):
			if neighborPos in closedSet: continue

			tentativeG = currentNode['g'] + 1

			if neighborPos not in openDict:
				neighbor = createNode(
					pos = neighborPos,
					g = tentativeG,
					h = heuristic(neighborPos, goals, treasures, treasureCollected),
					parent = currentNode
				)
				heapq.heappush(openList, (neighbor['f'], neighborPos))
				openDict[neighborPos] = neighbor
			elif tentativeG < openDict[neighborPos]['g']:
				# Found a better path to the neighbor
				neighbor = openDict[neighborPos]
				neighbor['g'] = tentativeG
				neighbor['f'] = tentativeG + neighbor['h']
				neighbor['parent'] = currentNode

	return [], 0


def createNode(pos: tuple[int, int],
               g: float = float('inf'),
               h: float = 0.0,
               parent: dict = None) -> dict:
	return {'pos': pos, 'g': g, 'h': h, 'f': g + h, 'parent': parent}


def getValidNeighbors(grid: list[list[int]],
                      pos: tuple[int, int]) -> list[tuple[int, int]]:
	x, y = pos
	rows = len(grid)
	cols = len(grid[0])
	possibleMoves = [
		(x+1, y), (x-1, y),
		(x, y+1), (x, y-1)
	]

	return [
		(nx, ny) for nx, ny in possibleMoves if
			0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'X'
	]


def reconstructPath(goalNode: dict) -> list[tuple[int, int]]:
	path = []
	current = goalNode

	while current is not None:
		path.append(current['pos'])
		current = current['parent']

	return path[::-1]


def heuristic(pos: tuple[int, int],
              goals: list[tuple[int, int]],
              treasures: list[tuple[int, int, int]],
              collected: int) -> int:
	if not goals: return 0
	if collected >= 5: return closestGoalDistance(pos, goals)
	return closestTreasureDistance(pos, goals, treasures)


def closestTreasureDistance(pos: tuple[int, int],
                            goals: list[tuple[int, int]],
                            treasures: list[tuple[int, int, int]]) -> int:
	treasureDistances = {t: manh(pos, (t[0], t[1])) for t in treasures}
	minDist = min(treasureDistances.values())
	minDistTreasures = [k for k, v in treasureDistances.items() if v == minDist]

	return min(closestGoalDistance((t[0], t[1]), goals) for t in minDistTreasures)


def closestGoalDistance(pos: tuple[int, int], goals: list[tuple[int, int]]) -> int:
	return min(manh(pos, g) for g in goals)

def manh(a: tuple[int, int], b: tuple[int, int]) -> int:
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


if __name__ == '__main__':
	print(pathfinding("../Examples/Example0/grid.txt"))
	print(pathfinding("../Examples/Example1/grid.txt"))
	print(pathfinding("../Examples/Example2/grid.txt"))
	print(pathfinding("../Examples/Example3/grid.txt"))
