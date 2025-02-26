from blocks import *
from collections import deque #allows pop, popleft, append, appendleft, 

# the game tree is a graph where each node is a game state and each edge is a legal move
# the tree is built breadth first, so the distance from the starting node is the depth of the node in the tree
# the tree is built until the goal state is found, or all nodes are exhausted

#note: it is overkill to have each node store an entire game, it really should just store the string representation
# the legal moves could have been recovered from this string. 

# nodes of the tree have the game, , a unique id = position in graph list,
# and the distance from the starting position node
class Node:
    def __init__(self, g: game, moves:dict, id:int, dist:int, parent:'Node', parEdge:tuple):
        self.game = g               # the game
        self.moves = moves          # the dict legal moves (piece, dir)->node
        self.id = id                # position in the graph list
        self.dist = dist            # distance from the starting position node
        self.parent = parent        # parent node (first one that discovered it)
        self.parEdge = parEdge         # edge from parent to this node
    def __str__(self):
        par = "None" if self.id==0 else self.parent.id 
        s=str(f"Node {self.id}, distance: {self.dist}, parent id={par}")+"\n"+str(self.game)
        for p,d in self.moves.keys():
            s += f"\n piece {p} moving {d} -> node {self.moves[(p,d)].id}"
        return s
    def __eq__(self, other):
        return self.game == other.game # no need to check other attributes, overruled by same game
    def __hash__(self):
        return hash(self.game)
    
    def pathBack(self):
        path = []
        node = self
        while node.id != 0:
            path.append(node.parEdge)
            node = node.parent
        s="" # string of solving moves from start to finish
        for p,d in reversed(path):
            s+=f"{p}-{d} "
        return f"this takes {self.dist} steps: {s}"