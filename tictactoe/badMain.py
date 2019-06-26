board = [["X", "X", "X"], ["4", "X", "6"], ["7", "8", "9"]]

# draw the board
for i in range(len(board)):
    for j in range(len(board[i])):
        print(board[i][j], end="")
        if (j < len(board[i]) - 1):
            print(" | ", end="")
    print()
    if (i != len(board)-1):
        print("----------")

def determineWin(isPlayerX):
    if (isPlayerX): symbol = "X"
    else: symbol = "O"
    
    # make sure the player has filled at least 3 squares
    numSquares = 0
    for i in board:
        for j in i:
            if (j == symbol): 
                numSquares = numSquares + 1
    if (numSquares < 3):
        return false

    # TODO check neighbors (check squares 1, 5, 9 first)



    return true

def getMatchingNeighbors(square):
    row = int((square-1)/3)
    col = (square-1)%3
    value = board[row][col]
    print(row, ",", col)

    illegalDirections = []
    if (row == 0): illegalDirections.append("up")
    if (col == 0): illegalDirections.append("left")
    if (row == len(board)): illegalDirections.append("down")
    if (col == len(board[0])): illegalDirections.append("right")
    print(col)
    print(illegalDirections)
    
    matchingNeighbors = []
    if ("up" not in illegalDirections and "left" not in illegalDirections):
        if (board[row-1][col-1] == value): matchingNeighbors.append((row-1)*3 + (col-1) + 1)
    if ("up" not in illegalDirections):
        if (board[row-1][col] == value): matchingNeighbors.append((row-1)*3 + col + 1)
    if ("up" not in illegalDirections and "right" not in illegalDirections):
        if (board[row-1][col+1] == value): matchingNeighbors.append((row-1)*3 + (col+1) + 1)
    if ("right" not in illegalDirections):
        if (board[row][col+1] == value): matchingNeighbors.append((row)*3 + (col+1) + 1)
    if ("down" not in illegalDirections and "right" not in illegalDirections):
        if (board[row+1][col+1] == value): matchingNeighbors.append((row+1)*3 + (col+1) + 1)
    if ("down" not in illegalDirections):
        if (board[row][col+1] == value): matchingNeighbors.append((row)*3 + (col+1) + 1)
    if ("down" not in illegalDirections and "left" not in illegalDirections):
        if (board[row+1][col-1] == value): matchingNeighbors.append((row+1)*3 + (col-1) + 1)
    if ("left" not in illegalDirections):
        if (board[row][col-1] == value): matchingNeighbors.append((row)*3 + (col-1) + 1)
    print(matchingNeighbors)

getMatchingNeighbors(3)