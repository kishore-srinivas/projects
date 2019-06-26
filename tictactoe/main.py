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

board = []
for i in range(9):
    board.append(Square(i))
board[0].setNeighbors([[board[1], Direction.EAST], [board[3], Direction.SOUTH], [board[4], Direction.SOUTHEAST]])
board[1].setNeighbors([[board[0], Direction.WEST], [board[2], Direction.EAST], [board[3], Direction.SOUTHWEST], [board[4], Direction.SOUTH], [board[5], Direction.SOUTHEAST]])
board[2].setNeighbors([[board[1], Direction.WEST], [board[4], Direction.SOUTHWEST], [board[5], Direction.SOUTH]])
board[3].setNeighbors([[board[0], Direction.NORTH], [board[1], Direction.NORTHEAST], [board[4], Direction.EAST], [board[7], Direction.SOUTHEAST], [board[6], Direction.SOUTH]])
board[4].setNeighbors([[board[0], Direction.NORTHWEST], [board[1], Direction.NORTH], [board[2], Direction.NORTHEAST], [board[3], Direction.WEST], [board[5], Direction.EAST], [board[6], Direction.SOUTHWEST], [board[7], Direction.SOUTH], [board[8], Direction.SOUTHEAST]])
board[5].setNeighbors([[board[4], Direction.WEST], [board[1], Direction.NORTHWEST], [board[2], Direction.NORTH], [board[8], Direction.SOUTH], [board[7], Direction.SOUTHWEST]])
board[6].setNeighbors([[board[3], Direction.NORTH], [board[4], Direction.NORTHEAST], [board[7], Direction.EAST]])
board[7].setNeighbors([[board[6], Direction.WEST], [board[3], Direction.NORTHWEST], [board[4], Direction.NORTH], [board[5], Direction.NORTHEAST], [board[8], Direction.EAST]])
board[8].setNeighbors([[board[7], Direction.WEST], [board[4], Direction.NORTHWEST], [board[5], Direction.NORTH]])


