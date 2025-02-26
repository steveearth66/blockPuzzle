from blocks import game

def testingAddRem(theBoard: game):
    print(theBoard)
    x = input("press + to add, - to remove, or x to exit: ")
    while x != "x":
        if x == "+":
            x = int(input ("piece to add 0-9: "))
            y=int(input("row: "))
            z=int(input("col: "))
            if not theBoard.addPiece(theBoard.pieces[x], (y,z)):
                    print("Error in adding piece")
        else:
            x = int(input("piece to remove 0-9: "))
            if not theBoard.removePiece(theBoard.pieces[x]):
                print("Error in removing piece")
        print(theBoard)
        x = input("press + to add, - to remove, or x to exit: ")
    return

def testMove(theBoard: game):
    print(theBoard)
    for p,d in theBoard.legalMoves():
        print(f"{p} can move {d}")
    x = input("press 0-9 piece to move or x to exit: ")
    while x != "x":
        x = int(x)
        y = input("press U,D,L,R direction: ").upper()
        if theBoard.movePiece(theBoard.pieces[x], y):
            print(theBoard)
            for p,d in theBoard.legalMoves():
                print(f"{p} can move {d}")
        else:
            print("Error in moving piece")
        x = input("press 0-9 piece to move or x to exit: ")
    return

theBoard = game()

# testMove(theBoard) #works well
# testingAddRem(theBoard) # works well