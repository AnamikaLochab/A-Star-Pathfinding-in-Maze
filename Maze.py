import pygame
import random
#import Algorithm1
size = 800
window = pygame.display.set_mode((size,size))

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
    def cell_row(self):
        return self.row
    def cell_column(self):
        return self.column
    def cell_position(self):
        return self.row, self.column
    def cell_blocked(self):
        self.color = (0,0,0)
        self.value = 0
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
    def update_agentmap(self,Grid): # I was planning to call this every time the agent moves so we can highlight all the blocks it's aware of so that we don't have to show 2 windows of the world and world according to agent
        #ignore for now
        if self.row > 0 :
            pygame.draw.line(window, (57, 255, 20), (self.x_cord , self.y_cord ), (self.x_cord , self.y_cord -self.width),5)
            pygame.draw.line(window, (57, 255, 20), (self.x_cord + self.width, self.y_cord), (self.x_cord + self.width, self.y_cord - self.width),5)
            pygame.draw.line(window, (57, 255, 20), (self.x_cord , self.y_cord-self.width), (self.x_cord + self.width, self.y_cord - self.width),5)
        if self.row < size//self.width -1:
            pygame.draw.line(window, (57, 255, 20), (self.x_cord , self.y_cord + self.width), (self.x_cord, self.y_cord + 2*self.width), 5)
            pygame.draw.line(window, (57, 255, 20), (self.x_cord + self.width, self.y_cord+ self.width),  (self.x_cord + self.width, self.y_cord + 2*self.width), 5)
            pygame.draw.line(window, (57, 255, 20), (self.x_cord, self.y_cord + 2*self.width), (self.x_cord + self.width, self.y_cord + 2*self.width), 5)

        if self.column > 0 :
            pass#pygame.draw.line(window, (57, 255, 20), (self.row, self.column), (self.row, self.column - 1))
        if self.row < size//self.width -1:
            pass#pygame.draw.line(window, (57, 255, 20), (self.row, self.column), (self.row, self.column+1))

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


def Assign_Start_End(Grid,rows,size):
    width = size // rows
    i = random.randint(0, rows - 1)
    j = random.randint(0, rows - 1)
    Start_Node = Grid[i][j]
    Grid[i][j].color = (255, 250, 0)
    # haven't put the loop to check if end nodes randomly gets same i,j as start, but will add that later
    i = random.randint(0, rows - 1)
    j = random.randint(0, rows - 1)
    End_Node = Grid[i][j]
    Grid[i][j].color = (255, 0, 0) # End node color red
    return Start_Node, End_Node



#def A_star():

def main(window, size):
    rows = 40
    G = grid(rows,size)
    play = True
    start = True

    while play:
        build_grid(window,size,rows)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if start:
            Start_Node, End_Node = Assign_Start_End(G,rows,size)
            draw_grid(window,G,rows,size)
            start = False
            #Algorithm1.A_Star(G,size,Start_Node,End_Node)
            pygame.display.update()




main(window,size)
