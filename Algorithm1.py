from MinHeap import MinHeap

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

    return path

    
def A_Star(Grid,size,Start_Node,End_Node):
    OpenSet=MinHeap(size)
    ClosedSet=[]
    OpenSet.insert(Start_Node)
    OpenSet.minHeap()
    PathTraversal=[]
    foundDest = False
    i = 0
    Start_Node.g = 0
    Start_Node.h = manhattanD(Start_Node,End_Node)
    Start_Node.f = Start_Node.cell_g() + Start_Node.cell_h()
    print(Start_Node.cell_f())
    while OpenSet.size>0:
        currentNode = OpenSet.remove()
        ClosedSet.append((currentNode.cell_row(), currentNode.cell_column()))
        # if currentNode !=Start_Node and currentNode!=End_Node:
        #     currentNode.color = (0,255,0)
        #     currentNode.draw_cell()
        # if(currentNode == End_Node):
        #     print("done")
        #     return True
        for n in currentNode.neighbours:
            if n.cell_row() == End_Node.cell_row() and n.cell_column() == End_Node.cell_column():
                n.parent = (currentNode.cell_row(), currentNode.cell_column())
                foundDest = True
                PathTraversal = tracePath(Grid, End_Node)
                return PathTraversal
            if (n.cell_row(), n.cell_column()) not in ClosedSet and n.value !=0:
                OpenSet.insert(n)
                OpenSet.minHeap()
                hTemp = manhattanD(n,End_Node)
                gTemp = currentNode.cell_g() + 1
                fTemp = hTemp + gTemp

                if fTemp < n.cell_f():
                    n.f = fTemp
                    n.g = gTemp
                    n.h = hTemp
                    n.parent = (currentNode.cell_row(), currentNode.cell_column() )
        
        print(str(currentNode.row) + ',' + str(currentNode.column))

    if not foundDest:
        print("No Path")
    return PathTraversal


def Repeated_A_Star(Grid,Size, StartNode,End_Node):
    S = StartNode
    # while S != End_Node and len(ClosedSet)!= 1600:
    #     S=A_Star(Grid,S,End_Node)
