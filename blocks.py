# puzzle based on blocks at museum of illusions

from enum import Enum

class Shape(Enum): #use as Shape.SING etc
    (SING, HORIZ, VERT, BIG) = range(1,5) # .value gives number 1-4

# ADJUSTABLE PARAMETERS (global)
rows, cols = 5,4 # size of the board
numPieces = [4,1,4,1] # number of single, horizontal, vertical, big pieces
starting = [(3,1),(3,2),(4,1),(4,2),# the singles. row x col with (0,0) at top left
                    (2,1), #the horizontal
                    (0,0),(0,3),(3,0),(3,3), # the verticals
                    (0,1)] # the big
finishLine = (3,1) # the exit location
goalPiece = 9 # the piece that must reach the exit
# END OF ADJUSTABLE PARAMETERS

dirs = {"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)} # directions for moving pieces
opps = {"U":"D","D":"U","L":"R","R":"L"} # opposite directions

class piece:
    def __init__(self, id: int=0, loc: tuple[int, int]=(-1,-1), shape: Shape=Shape.SING):
        self.id = id #could have just pointed to obj itself rather than id, but id=index in pieces list for lookup
        self.shape = shape
        self.loc = loc #location<->piece is referenced both via the piece and the board
    def __str__(self):
        return "SHVB"[self.shape.value-1] + str(self.id)
    def __eq__(self, other):
        return str(self) == str(other) #note: location not relevant to equality
    def __hash__(self):
        return hash(str(self))
    
    
def makePieces():
    pieces = []
    cumes = [0]+[sum(numPieces[:i+1]) for i in range(len(numPieces))] # this is needed to create the pieces with a nested for loop with proper id/shape
    for j in range(4):
        for i in range(cumes[j], cumes[j+1]):
            pieces.append(piece(i, shape=Shape(j+1)))
    return pieces

class game:
    def __init__(self):
        self.pieces = makePieces() #creates list of the ten pieces, all off the board
        self.board = [[-1 for i in range(cols)] for j in range(rows)] #creates empty board
        self.reset() #puts pieces onto the board in starting location
    def __str__(self):
        s = ""
        for i in range(rows):
            for j in range(cols):
                s += str(self.pieces[self.board[i][j]]) + " " if self.board[i][j] != -1 else ".. "
            s += "\n"
        return s[:-1]
    def __eq__(self, other):
        return str(self.board) == str(other.board)
    def __hash__(self):
        return hash(str(self.board))
    def copy(self):
        newGame = game()
        newGame.board = [row.copy() for row in self.board]  # deep copy of board
        newGame.pieces = [piece(p.id, p.loc, p.shape) for p in self.pieces] # deep copy of pieces
        return newGame
    def isSolved(self):
        return self.pieces[goalPiece].loc == finishLine

#returns True if piece correctly placed at loc, False otherwise
    def addPiece(self, p: piece, loc: tuple[int,int]): #assumes topmost leftmost corner of piece is at loc
        err=True #assume error, change to False when it actually accomplishes task
        if p.loc != (-1,-1) or loc[0]<0 or loc[1]<0 or loc[0]>=rows or loc[1]>=cols: # must pick up piece first
            return False
        if p.shape == Shape.SING and self.board[loc[0]][loc[1]] == -1:
            self.board[loc[0]][loc[1]] = p.id
            err = False
        elif p.shape == Shape.HORIZ and loc[1] < cols-1 and self.board[loc[0]][loc[1]] == -1 and self.board[loc[0]][loc[1]+1] == -1:
            self.board[loc[0]][loc[1]] = p.id
            self.board[loc[0]][loc[1]+1] = p.id
            err = False
        elif p.shape == Shape.VERT and loc[0] < rows-1 and self.board[loc[0]][loc[1]] == -1 and self.board[loc[0]+1][loc[1]] == -1:
            self.board[loc[0]][loc[1]] = p.id
            self.board[loc[0]+1][loc[1]] = p.id
            err = False
        else: # big piece
            if loc[0] < rows-1 and loc[1] < cols-1 and self.board[loc[0]][loc[1]] == -1 and self.board[loc[0]][loc[1]+1] == -1 and \
                self.board[loc[0]+1][loc[1]] == -1 and self.board[loc[0]+1][loc[1]+1] == -1:
                self.board[loc[0]][loc[1]] = p.id
                self.board[loc[0]][loc[1]+1] = p.id
                self.board[loc[0]+1][loc[1]] = p.id
                self.board[loc[0]+1][loc[1]+1] = p.id
                err=False
        if err:
            return False
        p.loc = loc
        return True
    
    # returns list of tuples of piece and direction that can be moved
    def legalMoves(self):
        moves = []
        for p in self.pieces:
            for d in dirs.keys():
                if self.movePiece(p, d):
                    moves.append((p, d))
                    self.movePiece(p, opps[d]) # move back to original position
        return moves

#returns True if piece correctly removed from loc, False otherwise    
    def removePiece(self, p: piece):
        err=True #assume error, change to False when it actually accomplishes task
        if p.loc == (-1,-1): 
            return False
        if p.shape == Shape.SING and self.board[p.loc[0]][p.loc[1]] == p.id:
            self.board[p.loc[0]][p.loc[1]] = -1
            err = False
        elif p.shape == Shape.HORIZ and p.loc[1] < cols-1 and self.board[p.loc[0]][p.loc[1]] == p.id and \
            self.board[p.loc[0]][p.loc[1]+1] == p.id:
            self.board[p.loc[0]][p.loc[1]] = -1
            self.board[p.loc[0]][p.loc[1]+1] = -1
            err = False
        elif p.shape == Shape.VERT and p.loc[0] < rows-1 and self.board[p.loc[0]][p.loc[1]] == p.id and \
            self.board[p.loc[0]+1][p.loc[1]] == p.id:
            self.board[p.loc[0]][p.loc[1]] = -1
            self.board[p.loc[0]+1][p.loc[1]] = -1
            err = False
        else: # big piece
            if p.loc[0] < rows-1 and p.loc[1] < cols-1 and self.board[p.loc[0]][p.loc[1]] == p.id and \
                self.board[p.loc[0]][p.loc[1]+1] == p.id and self.board[p.loc[0]+1][p.loc[1]] == p.id and \
                self.board[p.loc[0]+1][p.loc[1]+1] == p.id:
                self.board[p.loc[0]][p.loc[1]] = -1
                self.board[p.loc[0]][p.loc[1]+1] = -1
                self.board[p.loc[0]+1][p.loc[1]] = -1
                self.board[p.loc[0]+1][p.loc[1]+1] = -1
                err=False
        if err:
            return False
        p.loc = (-1,-1)
        return True

    def reset(self): # reset the board to the starting position
        for tile, pos in zip(self.pieces, starting):
            self.addPiece(tile, pos)
        return
       
    def movePiece(self, p: piece, dir: str):
        if dir not in dirs.keys():
            return False
        oldLoc = p.loc # save old location before removal erases it
        if not self.removePiece(p):
            return False
        x,y=dirs[dir]
        if not self.addPiece(p, (oldLoc[0]+x, oldLoc[1]+y)):
            self.addPiece(p, oldLoc) # put piece back if move failed
            return False
        return True