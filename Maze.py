import pygame
import random
import time

import sys

size = 800
window = pygame.display.set_mode((size,size))
count_cells=0

# Creating cell class with all properties and functions we might need for a particular cell
class cell :
	def __init__(self, row,column,width):
		self.color = (255,255,255) #White colour to all cells intitially
		self.row = row
		self.column = column
		self.value = 1
		self.width = width
		self.x_cord = row * width
		self.y_cord = column * width
		self.neighbours = []
		self.f = float('inf')
		self.g = float('inf')
		self.h = float('inf')
		self.parent = (-1, -1)

	def cell_row(self):
		return self.row
	def cell_column(self):
		return self.column
	def cell_position(self):
		return self.row, self.column
	def cell_blocked(self):
		self.color = (0,0,0)
		self.value = 0
	def cell_f(self):
		return self.f
	def cell_g(self):
		return self.g
	def cell_h(self):
		return self.h
	def cell_parent(self):
		return self.parent
	def draw_cell(self):
		pygame.draw.rect(window, self.color, (self.x_cord, self.y_cord,self.width, self.width))
	def draw_openset(self): #Don't know why I made this we can just change color using the variable and call draw_cell
		pygame.draw.rect(window, (20,252,20), (self.x_cord, self.y_cord, self.width, self.width))
	def cell_neighbours(self, Grid):
		self.neighbours=[]
		if self.row > 0 :
			self.neighbours.append(Grid[self.row - 1][self.column])
		if self.row < size//self.width -1:
			self.neighbours.append(Grid[self.row + 1][self.column])
		if self.column > 0 :
			self.neighbours.append(Grid[self.row][self.column - 1])
		if self.column< size//self.width -1:
			self.neighbours.append(Grid[self.row][self.column + 1])

class MinHeap:

	def __init__(self, maxsize):
		self.maxsize = maxsize
		self.size = 0
		self.Heap = [0]*(self.maxsize + 1)
		for i in range(maxsize):
			self.Heap[i] = cell(0, 0, 0)
			self.Heap[i].f = sys.maxsize
		self.Heap[0].f = -1*sys.maxsize
		self.FRONT = 1

	# Function to return the position of
	# parent for the node currently
	# at pos
	def parent(self, pos):
		return pos//2

	# Function to return the position of
	# the left child for the node currently
	# at pos
	def leftChild(self, pos):
		return 2 * pos

	# Function to return the position of
	# the right child for the node currently
	# at pos
	def rightChild(self, pos):
		return (2 * pos) + 1

	# Function that returns true if the passed
	# node is a leaf node
	def isLeaf(self, pos):
		return pos*2 > self.size

	# Function to swap two nodes of the heap
	def swap(self, fpos, spos):
		self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

	# Function to heapify the node at pos
	def minHeapify(self, pos):

		# If the node is a non-leaf node and greater
		# than any of its child
		if not self.isLeaf(pos):
			if (self.Heap[pos].cell_f() >= self.Heap[self.leftChild(pos)].cell_f() or
			self.Heap[pos].cell_f() >= self.Heap[self.rightChild(pos)].cell_f()):

				# Swap with the left child and heapify
				# the left child
				if self.Heap[self.leftChild(pos)].cell_f() < self.Heap[self.rightChild(pos)].cell_f():
					if self.Heap[self.leftChild(pos)].cell_f() == self.Heap[pos].cell_f():
						if self.Heap[pos].cell_g() < self.Heap[self.leftChild(pos)].cell_g():
							self.swap(pos, self.leftChild(pos))
							self.minHeapify(self.leftChild(pos))
					else:
						self.swap(pos, self.leftChild(pos))
						self.minHeapify(self.leftChild(pos))

				if self.Heap[self.leftChild(pos)].cell_f() == self.Heap[self.rightChild(pos)].cell_f():
					if self.Heap[self.leftChild(pos)].cell_g() > self.Heap[self.rightChild(pos)].cell_g():
						if self.Heap[pos].cell_f() == self.Heap[self.leftChild(pos)].cell_f():
							if self.Heap[pos].cell_g() < self.Heap[self.leftChild(pos)].cell_g():
								self.swap(pos, self.leftChild(pos))
								self.minHeapify(self.leftChild(pos))
						else:
							self.swap(pos, self.leftChild(pos))
							self.minHeapify(self.leftChild(pos))
					else:
						if self.Heap[pos].cell_f() == self.Heap[self.rightChild(pos)].cell_f():
							if self.Heap[pos].cell_g() < self.Heap[self.rightChild(pos)].cell_g():
								self.swap(pos, self.rightChild(pos))
								self.minHeapify(self.rightChild(pos))
						else:
							self.swap(pos, self.rightChild(pos))
							self.minHeapify(self.rightChild(pos))

						

				# Swap with the right child and heapify
				# the right child
				else:
					if self.Heap[self.leftChild(pos)].cell_f() == self.Heap[pos].cell_f():
						if self.Heap[pos].cell_g() < self.Heap[self.rightChild(pos)].cell_g():
							self.swap(pos, self.rightChild(pos))
							self.minHeapify(self.rightChild(pos))
					else:
						self.swap(pos, self.rightChild(pos))
						self.minHeapify(self.rightChild(pos))
					

	# Function to insert a node into the heap
	def insert(self, element):
		if self.size >= self.maxsize :
			return
		self.size+= 1
		self.Heap[self.size] = element

		current = self.size

		while self.Heap[current].cell_f() <= self.Heap[self.parent(current)].cell_f():
			# For tie-breaking
			# if self.Heap[current].cell_f() == self.Heap[self.parent(current)].cell_f():
			# 	if self.Heap[current].cell_g() > self.Heap[self.parent(current)].cell_g():
			# 		self.swap(current, self.parent(current))
			# 		current = self.parent(current)
			# 	else:
			# 		break
			
			self.swap(current, self.parent(current))
			current = self.parent(current)

	# Function to print the contents of the heap
	def Print(self):
		for i in range(1, (self.size//2)+1):
			print(" PARENT : "+ str(self.Heap[i])+" LEFT CHILD : "+
								str(self.Heap[2 * i])+" RIGHT CHILD : "+
								str(self.Heap[2 * i + 1]))

	# Function to build the min heap using
	# the minHeapify function
	def minHeap(self):

		for pos in range(self.size//2, 0, -1):
			self.minHeapify(pos)

	# Function to remove and return the minimum
	# element from the heap
	def remove(self):

		popped = self.Heap[self.FRONT]
		self.Heap[self.FRONT] = self.Heap[self.size]
		self.size-= 1
		self.minHeapify(self.FRONT)
		return popped

# grid function uses the cell class and 2D array named grid to create the gridworld and also chooses random blocked cells
def grid(rows,size):
	Grid = []    #List to 2D array
	width = size//rows
	for i in range(rows):
		Grid.append([])
		for j in range(rows):
			c = cell(i,j,width)
			r = random.choice([0, 1, 2, 3,4])  # need to add the random function with probability to chose blocked but this works for now
			if (r == 0):
				c.cell_blocked() # the cell class has this function and sets color to black
			Grid[i].append(c)
	return Grid

# agent_grid function uses the cell class and 2D array named grid to create the gridworld for the agent
def agent_grid(rows,size):
	Grid = []    #List to 2D array
	width = size//rows
	for i in range(rows):
		Grid.append([])
		for j in range(rows):
			c = cell(i,j,width)
			Grid[i].append(c)
	return Grid

# reset the f, g, h, and parent values of the agent grid for the next call of A*
def clear_values(Grid,adaptive=False):
	for i in range(len(Grid)):
		for j in range(len(Grid[i])):
			Grid[i][j].f = float('inf')
			Grid[i][j].g = float('inf')
			if not adaptive:
				Grid[i][j].h = float('inf')
			Grid[i][j].parent = (-1, -1)

# build_grid just draws the lines based on
def build_grid(window, size, rows) :
	width = size//rows
	x =0
	y =0
	for i in range(rows):
		x += width
		y +=width
		pygame.draw.line(window,(0,0,0),(x,0),(x,size))
		pygame.draw.line(window, (0,0,0),(0,y), (size, y))

#Not sure if we need neighbours we can just change i,j and voila but just in case to make it look nce
def Neighbous( Grid):
	for G in Grid:
		for cell in G:
			cell.cell_neighbours(Grid)

#draw_grid iterates through each cell object ing Grid and draw_cell checks colors and draws cells obviously
def draw_grid(window,Grid, rows, size):
	width = size//rows
	window.fill((255, 255, 255))
	for G in Grid:
		for cell in G:
			cell.draw_cell()

	build_grid(window,size,rows)
	Neighbous(Grid)
	Screen = pygame.display.update()


def Assign_Start_End(Grid, AgentGrid, rows,size):
	width = size // rows
	i = 0
	j = 1
	if Grid[i][j].value == 0:
		Grid[i][j].value == 1
	Start_Node = AgentGrid[i][j]
	AgentGrid[i][j].color = (255, 250, 0) # Start node color yellow

	i = rows - 1
	j = rows - 2
	if Grid[i][j].value == 0:
		Grid[i][j].value = 1

	End_Node = AgentGrid[i][j]
	AgentGrid[i][j].color = (255, 0, 0) # End node color red

	return Start_Node, End_Node

def manhattanD(cell1,cell2):
	x = abs(cell1.cell_row() - cell2.cell_row())
	y = abs(cell1.cell_column() - cell2.cell_column())
	return x + y

def tracePath(Grid, End_Node):
	row = End_Node.cell_row()
	col = End_Node.cell_column()

	path = []

	while(not Grid[row][col].parent == (row, col)):
		path.insert(0, (row, col))
		temp_row = Grid[row][col].parent[0]
		temp_col = Grid[row][col].parent[1]
		row = temp_row
		col = temp_col

	return path 

	
def A_Star(Grid,size,Start_Node,End_Node,adaptive=False):
	OpenSet=MinHeap(10000)
	ClosedSet=[]
	OpenSet.insert(Start_Node)
	PathTraversal=[]
	foundDest = False
	i = 0
	Start_Node.g = 0
	Start_Node.h = manhattanD(Start_Node,End_Node)
	Start_Node.f = Start_Node.cell_g() + Start_Node.cell_h()
	Start_Node.parent = (Start_Node.cell_row(), Start_Node.cell_column())

	while OpenSet.size>0:
		currentNode = OpenSet.remove()
		global count_cells
		count_cells = count_cells+1
		ClosedSet.append((currentNode.cell_row(), currentNode.cell_column()))
		for n in currentNode.neighbours:
			if n.cell_row() == End_Node.cell_row() and n.cell_column() == End_Node.cell_column():
				n.parent = (currentNode.cell_row(), currentNode.cell_column())
				foundDest = True
				PathTraversal = tracePath(Grid, End_Node)
				return PathTraversal
			if (n.cell_row(), n.cell_column()) not in ClosedSet and n.value !=0:
				if(adaptive):																		#for adaptive runs			
					S_to_goal=manhattanD(n,End_Node)
					S_to_current=manhattanD(n,Start_Node)
					if(n.h == float('inf')):														#infinite h values use normal heuristic
						n.h =manhattanD(n,End_Node)
					else:
						n.h=S_to_goal-S_to_current													#heuristic changes for adaptive runs
					n.g=currentNode.cell_g()+1	
					n.f=n.g+n.h
					n.parent = (currentNode.cell_row(), currentNode.cell_column() )
					OpenSet.insert(n)	

				else:																				#for normal runs
					hTemp = manhattanD(n,End_Node)
					gTemp = currentNode.cell_g() + 1
					fTemp = hTemp + gTemp

					if fTemp < n.cell_f():
						n.f = fTemp
						n.g = gTemp
						n.h = hTemp
						n.parent = (currentNode.cell_row(), currentNode.cell_column() )
						OpenSet.insert(n)
		OpenSet.minHeap()

	if not foundDest:
		print("No Path")
	return PathTraversal


def Repeated_A_Star(Grid, AgentGrid, size, StartNode,End_Node,adaptive=False):
	S = StartNode
	Grid[S.cell_row()][S.cell_column()].color=(255,250,0)

	counter=0

	while S.cell_row() != End_Node.cell_row() or S.cell_column() != End_Node.cell_column():
		if(adaptive):
			path = A_Star(AgentGrid, size, S, End_Node,counter != 0)				#for the first call, the adaptive A* runs like normal A*
		else:
			path=A_Star(AgentGrid,size,S,End_Node)
		counter+=1																	#counter to keep track of A* calls

		if len(path) == 0:
			print("I cannot reach the target")
			return
		endOfPath = -1
		for i in range(len(path)):
			current = path[i]
			row = current[0]
			col = current[1]
			if AgentGrid[row][col].value == 0 or path[i] == (End_Node.cell_row(),End_Node.cell_column()):
				endOfPath = i
				break
			for n in AgentGrid[row][col].neighbours:
				if Grid[n.cell_row()][n.cell_column()].value == 0:
					n.value = 0
					n.color = (0,0,0)

		for i in range(endOfPath):
			current = path[i]
			row = current[0]
			col = current[1]
			if row != End_Node.cell_row() or col != End_Node.cell_column():
				AgentGrid[row][col].color = (0,255,0)
				AgentGrid[row][col].draw_cell()
				Grid[row][col].color=(0,255,0)

		S = AgentGrid[path[endOfPath - 1][0]][path[endOfPath - 1][1]]
		if not (path[endOfPath] == (End_Node.cell_row(),End_Node.cell_column())):
			Grid[path[endOfPath - 1][0]][path[endOfPath - 1][1]].color=(0,0,255)
		S.color = (0, 0, 255)
		S.draw_cell()
		clear_values(AgentGrid,adaptive)												#remembering the h values for nodes that have been travesered in adaptive A* calls
		


		Grid[End_Node.cell_row()][End_Node.cell_column()].color=(255,0,0)
		draw_grid(window,Grid,100,size)
	Grid[End_Node.cell_row()][End_Node.cell_column()].color=(255,0,0)
	print("I reached the target")
		
def Repeated_Backward_A_Star(Grid, AgentGrid, size, StartNode,End_Node,adaptive=False):
	Repeated_A_Star(Grid, AgentGrid, size, End_Node, StartNode, adaptive)

def main(window, size):
	rows = 100
	G = grid(rows,size)
	AG = agent_grid(rows,size)
	play = True
	start = True

	while play:
		build_grid(window,size,rows)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		if start:
			Start_Node, End_Node = Assign_Start_End(G,AG,rows,size)
			for n in AG[Start_Node.cell_row()][Start_Node.cell_column()].neighbours:
				if G[n.cell_row()][n.cell_column()].value == 0:
					n.value = 0
					n.color = (0, 0, 0)
			draw_grid(window,AG,rows,size)
			start = False
			startTime=time.time()
			path = Repeated_A_Star(G,AG,size,Start_Node,End_Node) 			#using True and False for repeated or Adapative A* runs
			endTime=time.time()
			print('Forward A*: ',count_cells)
			print('Time Taken: ', endTime-startTime)
			count_repeated=count_cells
			startTime=time.time()
			path2=Repeated_A_Star(G,AG,size,Start_Node,End_Node,True)
			endTime=time.time()
			print('Adaptive A*: ',count_cells-count_repeated)
			print('Time Taken: ', endTime-startTime)
			start=False
			pygame.display.update()




main(window,size)