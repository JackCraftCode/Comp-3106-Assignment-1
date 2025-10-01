import csv
import heapq


# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath) -> tuple[list[tuple[int, int]], int ,int]:
	grid = []
	start = None
	goals = []
	walls = []
	treasures = []

	with open(filepath, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			grid.append(row)

	r = len(grid)
	c = len(grid[0])

	for row in range(r):
		for col in range(c):
			temp = grid[row][col]
			if temp == 'S':
				start = (row, col)
			elif temp == 'G':
				goals.append((row, col))
			elif temp.isdigit() and int(temp) > 0:
				treasures.append((row, col, int(temp)))
			elif temp == 'X':
				walls.append((row, col))

	path, explored = aStarSearch(grid, start, goals, walls, treasures)
	cost = max(0, len(path) - 1)
	return path, cost, explored


def aStarSearch(grid: list[list[int]],
                start: tuple[int, int],
                goals: list[tuple[int, int]],
                walls: list[tuple[int, int]],
                treasures: list[tuple[int, int, int]]) -> tuple[list[tuple[int, int]] ,int]:
	startNode = createNode(
		pos = start,
		treasureValue = 0,
		g = 0,
		h = heuristic(start, goals, treasures, 0)
	)

	explored = 0
	startState = (start, startNode['treasureValue'], startNode['treasureCollected'])
	openList = [startState]            # Priority queue
	openDict = {startState: startNode} # For quick node lookup
	closedSet = set()                  # Explored nodes

	while openList:
		state = heapq.heappop(openList)
		if state in closedSet: continue
		curPos, treasureValue, treasureCollected = state
		curNode = openDict[state]

		if curPos in goals and treasureValue >= 5:
			return reconstructPath(curNode), explored

		explored += 1
		closedSet.add(state)

		for nPos in getValidNeighbors(curPos, (len(grid), len(grid[0])), walls):
			nVal = treasureValue
			nCol = treasureCollected

			v = next((v for x, y, v in treasures if (x, y) == nPos), None)

			if v is not None and nPos not in nCol:
				nVal = treasureValue + v
				nCol = frozenset(set(treasureCollected) | {nPos})

			nState = (nPos, nVal, nCol)
			if nState in closedSet: continue

			tentativeG = curNode['g'] + 1
			prev = openDict.get(nState)
			if prev is None or tentativeG < prev['g']:
				neighbor = createNode(
					pos = nPos,
					treasureValue = nVal,
					treasureCollected = nCol,
					g = tentativeG,
					h = heuristic(nPos, goals, treasures, curNode['treasureValue']),
					parent = curNode
				)
				openDict[nState] = neighbor
				heapq.heappush(openList, nState)

	return [], 0


def createNode(pos: tuple[int, int],
               treasureValue: int,
               treasureCollected: tuple[tuple[int, int]] = tuple(),
               g: float = float('inf'),
               h: int = 0,
               parent: dict = None) -> dict:
	return {'pos': pos, 'treasureValue': treasureValue, 'treasureCollected': treasureCollected,
	        'g': g, 'h': h, 'f': g + h, 'parent': parent}


def getValidNeighbors(pos: tuple[int, int], size: tuple[int, int],
                      walls: list[tuple[int, int]]) -> list[tuple[int, int]]:
	x, y = pos
	r, c = size

	return [
		(nx, ny) for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)) if
			0 <= nx < r and 0 <= ny < c and (nx, ny) not in walls
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

	return min(closestGoalDistance((t[0], t[1]), goals) for t in minDistTreasures) + minDist


def closestGoalDistance(pos: tuple[int, int], goals: list[tuple[int, int]]) -> int:
	return min(manh(pos, g) for g in goals)


def manh(a: tuple[int, int], b: tuple[int, int]) -> int:
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


if __name__ == '__main__':
	print(pathfinding("../Examples/Example0/grid.txt"))
	print(pathfinding("../Examples/Example1/grid.txt"))
	print(pathfinding("../Examples/Example2/grid.txt"))
	print(pathfinding("../Examples/Example3/grid.txt"))
