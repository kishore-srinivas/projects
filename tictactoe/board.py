from square import Square
from enum import Enum, auto

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
        
class Direction(AutoName):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    NORTHEAST = auto()
    NORTHWEST = auto()
    SOUTHEAST = auto()
    SOUTHWEST = auto()
    
    def getOpposite(self):
        if (self == self.NORTH): return self.SOUTH
        if (self == self.SOUTH): return self.NORTH
        if (self == self.EAST): return self.WEST
        if (self == self.WEST): return self.EAST
        if (self == self.NORTHWEST): return self.SOUTHEAST
        if (self == self.NORTHEAST): return self.SOUTHWEST
        if (self == self.SOUTHWEST): return self.NORTHEAST
        if (self == self.SOUTHEAST): return self.NORTHWEST

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        board = self.board

        for i in range(width*height):
            board.append(Square(i))
        for i in range(len(board)):
            neighbors = self.calculateNeighbors(i)
            print(i, ":", neighbors)
            for n in neighbors:
                board[i].addNeighbor([board[n[0]], n[1]])
            print(i, ":", board[i].getNeighbors())

    def getSize(self):
        return self.width * self.height

    def get(self, index):
        return self.board[index]
        
    def draw(self):
        board = self.board
        print(" ", board[0].getValue(), "|", board[1].getValue(), "|", board[2].getValue())
        print("  ----------")
        print(" ", board[3].getValue(), "|", board[4].getValue(), "|", board[5].getValue())
        print("  ----------")
        print(" ", board[6].getValue(), "|", board[7].getValue(), "|", board[8].getValue())

    def isWinner(self, player, lastPlaced):
        board = self.board
        candidates = board[lastPlaced].getMatchingNeighbors()

        # checks for candidates on opposite sides of the current square
        for c in candidates:
            for c2 in candidates:
                if (c[1] == c2[1].getOpposite()):
                    return True

        # pursue lines in the directions of the matching neighbors
        while (len(candidates) > 0):
            toCheck = candidates[0]
            print("toCheck:", toCheck)
            secondaryNeighbors = toCheck[0].getMatchingNeighbors()
            for s in secondaryNeighbors:
                if (s[1] == toCheck[1]):
                    print(s[0].getLocation())
                    print(toCheck[0].getLocation())
                    return True
            candidates.remove(candidates[0])

        return False

    def calculateNeighbors(self, square):
        width = self.width
        height = self.height

        if (square > width*height-1 or square < 0):
            return [-1, -1]

        row = int(square/width)
        col = square % width

        neighbors = []
        neighbors.append([(row-1)*width + col, Direction.NORTH])
        neighbors.append([(row-1)*width + (col+1), Direction.NORTHEAST])
        neighbors.append([row*width + (col+1), Direction.EAST])
        neighbors.append([(row+1)*width + (col+1), Direction.SOUTHEAST])
        neighbors.append([(row+1)*width + col, Direction.SOUTH])
        neighbors.append([(row+1)*width + (col-1), Direction.SOUTHWEST])
        neighbors.append([row*width + (col-1), Direction.WEST])
        neighbors.append([(row-1)*width + (col-1), Direction.NORTHWEST])
        
        # remove neighbors that do not apply
        global i
        i = 0
        while (i < len(neighbors)):
            # if cell is in top row remove all neighbors to the north
            if (row == 0):
                if (neighbors[i][1] == Direction.NORTH or neighbors[i][1] == Direction.NORTHWEST or neighbors[i][1] == Direction.NORTHEAST):
                    neighbors.remove(neighbors[i])
                    i = i - 1
            # if cell is in bottom row remove all neighbors to the south
            if (row == height - 1):
                if (neighbors[i][1] == Direction.SOUTH or neighbors[i][1] == Direction.SOUTHWEST or neighbors[i][1] == Direction.SOUTHEAST):
                    neighbors.remove(neighbors[i])
                    i = i - 1        
            # if cell is in left column remove all neighbors to the west
            if (col == 0):
                if (neighbors[i][1] == Direction.WEST or neighbors[i][1] == Direction.SOUTHWEST or neighbors[i][1] == Direction.NORTHWEST):
                    neighbors.remove(neighbors[i])
                    i = i - 1             
            # if cell is in right column remove all neighbors to the east
            if (col == width - 1):
                if (neighbors[i][1] == Direction.EAST or neighbors[i][1] == Direction.NORTHEAST or neighbors[i][1] == Direction.SOUTHEAST):
                    neighbors.remove(neighbors[i])
                    i = i - 1 
            i = i + 1

        return neighbors
