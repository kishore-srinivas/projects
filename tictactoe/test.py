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
        
print(Direction.NORTH)
print(Direction.NORTH.getOpposite())