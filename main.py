from blocks import game, goalPiece, finishLine
from gameTree import Node
from collections import deque #allows pop, popleft, append, appendleft
from heapq import heappush, heappop #allows push and pop with priority queue

gameGraph = deque() # list of all currently constructed nodes in the game tree (possibly incomplete)
boundary = [] # list of all nodes on the boundary. i.e. the edges have not yet been computed
stateDict = dict() # dictionary of game states to node id's for fast lookup of existing nodes
edgeCount = 0
priority = [finishLine,(3,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,1)] #heuristic for boundary priority queue based on Big position
# priority = [finishLine,(3,2),(2,2),(2,1),(2,0),(1,0),(0,0),(0,1)] #other direction still doesn't find optimal first

def ranking(theNode: Node) -> int:
    pos = theNode.game.pieces[goalPiece].loc
    try :
        return priority.index(pos)  # return the index of the position in the priority list
    except ValueError:
        return 8 #if you're not close to our believed optimal path, you're at the end of the line

startGame = game()
startNode = Node(g=startGame, moves={}, id=len(gameGraph), dist=0, parent=None, parEdge=None)
solutions = []
stateDict[startNode.game] = startNode.id
gameGraph.append(startNode)
heappush(boundary, (ranking(startNode), startNode.id, startNode)) # add the start node to the boundary. id required for tiebreakers
#boundary.append(startNode)
maxDist = 0
# really this would be for all members of boundary
while solutions==[]:
#while boundary!=[]:
    # get the next node from the boundary
    # saveNode = boundary.popleft()
    saveNode = heappop(boundary)[2] #gets the game from the tuple
    edges = saveNode.game.legalMoves()
    edgeCount += len(edges)
    for p,d in edges:
        copyGame = saveNode.game.copy() #needed since moving mutates board rather than returning a new game
        copiedPiece = copyGame.pieces[p.id]
        copyGame.movePiece(copiedPiece, d) # make the move
        if copyGame in stateDict: # O(1) lookup of the node vs O(n) checking .keys()
            saveNode.moves[(p,d)] = gameGraph[stateDict[copyGame]]
        else:
            newNode = Node(g=copyGame, moves={}, id=len(gameGraph), dist=saveNode.dist+1, \
                           parent=saveNode, parEdge=(p,d))
            if newNode.id % 10000 == 0:
                print(f"completed node {newNode.id}/14,950,00 at dist={newNode.dist}/197")
            stateDict[newNode.game] = newNode.id # add to dictionary for future lookups
            if newNode.dist > maxDist: # for progress bar
                maxDist = newNode.dist
                #print(f"new max distance: {maxDist}/197 found at node {newNode.id}/14,950,080. left in boundary={len(boundary)}")
            if newNode.game.isSolved():
                solutions.append(newNode)
                #print(f"Completed node {newNode.id}")
                #print(newNode.pathBack())
                #x= input("press enter to continue")
            gameGraph.append(newNode)
            #boundary.append(newNode)
            heappush(boundary, (ranking(newNode), newNode.id, newNode))
            saveNode.moves[(p,d)] = newNode

''' use when While loop goes through entire tree and not just looking for first solution
print(f"found {len(solutions)}/555264 solutions with {len(gameGraph)} possible states and {edgeCount} edges")
print(f"max distance from start is {maxDist}/197")
print(f"{gameGraph[-1].game}")
print(gameGraph[-1].pathBack())
print()
print(f"first solution found at node {solutions[0].id}")
print(solutions[0].pathBack())
'''

print(f"first solution found at node {solutions[0].id}")
print(solutions[0].pathBack())

'''
our heuristic, while speedy, does not find the optimal solution.
It finds a solution in 118 moves, while the optimal solution is 112 moves.
H4-L S1-U S1-R H4-R V7-U S2-L S3-L V8-L S1-D S1-D H4-R S0-U S3-U S2-R V7-D S0-L H4-L V6-D V6-D B9-R V5-R S0-U S0-U V7-U S2-L V7-U S3-L V8-L S1-L S1-U V6-D H4-R 
V8-U S2-R S2-R V8-D V5-D S0-R V7-U S3-U V8-L V5-D V5-D S3-R S3-U H4-L H4-L V6-U S2-R S1-D V6-L S2-U S1-R V6-D H4-R H4-R V5-U V7-D S0-L S3-U V5-U V6-L S1-L S2-D 
H4-D B9-D S3-R S0-R S3-R S0-R V5-U V6-U S1-L S2-L V7-U V8-U S1-L S2-L H4-D B9-D S0-D S0-R V5-R V6-U V6-U B9-L S0-D S0-D S3-D S3-D V5-R V6-R V7-R V8-U V8-U B9-L 
S0-L S0-U H4-U S2-R S1-R S2-R S1-R B9-D S0-L S0-L S3-L S3-L H4-U S1-U S1-R B9-R

computing the entire tree shows that there are 14,950,080 nodes and 48,324,096 edges and 555,264 solution states.
a state with the highest distance from the start is 197 moves away
.. V5 V7 S0
S2 V5 V7 ..
S3 V8 H4 H4
V6 V8 B9 B9
V6 S1 B9 B9
H4-R V7-U S2-L S0-D V7-R S2-U S0-L V7-D H4-L H4-L S1-U S1-R S3-U S3-U V7-R S0-R S2-D H4-D S3-L S1-L S3-L S1-L V7-U S0-R S2-R V8-U S0-R S2-R H4-D S1-D S3-R V5-D V5-D 
B9-L V6-L V8-U V8-U V7-R S2-U S0-L S2-U S0-U H4-R V5-D S3-L S2-L S0-U V7-D S0-R V6-D V6-D B9-R S3-U S2-L S1-U S3-U S2-U S1-L V6-L S0-L S0-D V7-U H4-R V6-D B9-D S3-R 
S2-U S1-U S3-R S2-R S1-U V5-U V5-U V6-L S0-L S0-D B9-D S3-D S3-L V8-L V7-U V7-U B9-R S0-U S3-D S2-D S1-R H4-L V5-U V6-U H4-L B9-D S3-R S2-D S1-D S3-R S2-R S1-D V8-L 
S2-U S2-U S3-L S3-U B9-U H4-R H4-R S0-D S0-L S1-D S1-D V8-D V8-D V5-R V6-U V6-U V8-L B9-L V7-D S2-R V7-D S3-R V5-R V6-R V8-U V8-U B9-L V5-D S2-L S3-U V7-U H4-U S1-R 
S0-R S1-R S0-R B9-D V6-D S2-L S3-L V7-U V8-D S2-L S3-L V5-U H4-U S1-U S0-R B9-R V8-D V8-D V6-L S3-D S2-R H4-L S1-U V6-U H4-L S1-L V7-D V7-D V5-R S1-U H4-R V6-D S2-L 
S3-U S1-L V5-L V7-U S0-U V7-U H4-R S1-D S3-D S2-R V6-U S1-L H4-L S0-U B9-R V8-R S1-D S1-D V6-D S2-L V6-D S3-L V5-L V7-L S0-U S0-U H4-R V8-U S1-R V6-D S3-D S2-D

'''