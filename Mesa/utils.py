
from pandas import *
from .minHeap import MinHeap

def obtenerAgente(grid, posicion):
    elementos = grid.get_neighborhood(posicion, False, True)
    iterable = grid.iter_cell_list_contents(elementos)

    for elemento in iterable: 
        if elemento.pos == posicion: 
            return elemento

def getPosCorrectaGrid(matrix, pos): 
    return (pos[1], len(matrix)-1 - pos[0])

class Node:
    def __init__(self, row, col, value):
        self.id = str(row) + "-" + str(col)
        self.row = row
        self.col = col 
        self.value = value
        self.distanceFromStart = float('inf')
        self.estimatedDistanceToEnd = float("inf")
        self.cameFrom = None
        

def AStar(startRow, startCol, endRow, endCol, graph, sentido):
    nodes = initializeNodes(graph)
	
    startNode = nodes[startRow][startCol]
    endNode = nodes[endRow][endCol]
	
    startNode.distanceFromStart = 0
    startNode.estimatedDistanceToEnd = calculateManhattanDistance(startNode, endNode)
	
    nodesToVisit = MinHeap([startNode])
	
    while not nodesToVisit.isEmpty():
        currentMinDistanceNode = nodesToVisit.remove()
		
        if currentMinDistanceNode == endNode:
            break
			
        neighbors = getNeighboringNodes(currentMinDistanceNode, nodes)
        for neighbor in neighbors:
            if neighbor.value == 0:
                continue
			
            tentativeDistanceToNeighbor = currentMinDistanceNode.distanceFromStart + 1
			
            if tentativeDistanceToNeighbor >= neighbor.distanceFromStart:
                continue
				
            neighbor.cameFrom = currentMinDistanceNode
            neighbor.distanceFromStart = tentativeDistanceToNeighbor
            neighbor.estimatedDistanceToEnd = tentativeDistanceToNeighbor + calculateManhattanDistance(
				neighbor, endNode
			)
			
            if not nodesToVisit.containsNode(neighbor):
                nodesToVisit.insert(neighbor)
            else:
                nodesToVisit.update(neighbor)
		
    return reconstructPath(endNode)

def initializeNodes(graph):
	nodes = []
	
	for i, row in enumerate(graph):
		nodes.append([])
		for j, value in enumerate(row):
			nodes[i].append(Node(i, j, value))
			
	return nodes

def calculateManhattanDistance(currentNode, endNode):
	currentRow = currentNode.row
	currentCol = currentNode.col
	endRow = endNode.row
	endCol = endNode.col
	
	return abs(currentRow - endRow) + abs(currentCol - endCol)

def getNeighboringNodes(node, nodes):
	neighbors = []
	
	numRows = len(nodes)
	numCols = len(nodes[0])

	row = node.row
	col = node.col
	
	if row < numRows - 1:
		neighbors.append(nodes[row + 1][col])
		
	if row > 0:
		neighbors.append(nodes[row - 1][col])
		
	if col < numCols - 1:
		neighbors.append(nodes[row][col + 1])
		
	if col > 0:
		neighbors.append(nodes[row][col - 1])
		
	return neighbors

def reconstructPath(endNode):
	if not endNode.cameFrom:
		return []
	
	currentNode = endNode
	path = []
	
	while currentNode is not None:
		path.append([currentNode.row, currentNode.col])
		currentNode = currentNode.cameFrom
	return path[::-1]
