OpenSet=[]
ClosedSet=[]
def manhattanD(cell1,cell2):
    x = abs(cell1.cell_row() - cell2.cell_row())
    y = abs(cell1.cell_column() - cell2.cell_column())
    return x + y
def A_Star(Grid,size,Start_Node,End_Node):
    OpenSet.append(Start_Node)
    PathTraversal=[]
    i = 0
    h_score = {}
    g_score = {}
    f_score = {}
    g_score[Start_Node]=0
    h_score[Start_Node] = manhattanD(Start_Node,End_Node)
    f_score[Start_Node] = g_score[Start_Node] + h_score[Start_Node]
    print(f_score[Start_Node])
    while len(OpenSet)>0:
        currentNode = OpenSet[0]
        for i in range(0,len(OpenSet)):
            if(f_score[OpenSet[i]]<=f_score[currentNode] ):
                currentNode = OpenSet[i]
        OpenSet.remove(currentNode)
        ClosedSet.append(currentNode)
        print(f_score[currentNode], "f--g",g_score[currentNode], "h ",h_score[currentNode],"  --" , currentNode.cell_row() , "row -- Column", currentNode.cell_column())
        if currentNode !=Start_Node and currentNode!=End_Node:
            currentNode.color = (0,255,0)
            currentNode.draw_cell()
        if(currentNode == End_Node):
            print("done")
            return True
        OpenSet.clear()
        for n in currentNode.neighbours:
            if n not in ClosedSet and n.value !=0:
                OpenSet.append(n)
                h_score[n] = manhattanD(n,End_Node)
                g_score[n] = g_score[currentNode]+1
                f_score[n] = g_score[n]+ h_score[n]
                print(f_score[n])
    print("No Path")
def Repeated_A_Star(Grid,Size, StartNode,End_Node):
    S = StartNode
    while S != End_Node and len(ClosedSet)!= 1600:
        S=A_Star(Grid,S,End_Node)

