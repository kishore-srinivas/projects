class Square:

    def __init__(self, location):
        self.value = " "
        self.location = location
        self.neighbors = []

    def setValue(self, newValue):
        self.value = newValue

    def getValue(self):
        return self.value

    def isEmpty(self):
        if (self.value == " "):
            return True
        return False

    def getLocation(self):
        return self.location

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def getNeighbors(self):
        return self.neighbors

    def getNeighbor(self, direction):
        for n in self.getNeighbors():
            if n[1] == direction:
                return n

    def getMatchingNeighbors(self):
        matchingNeighbors = []
        for n in self.getNeighbors():
            if n[0].getValue() == self.value:
                matchingNeighbors.append(n)
        return matchingNeighbors

    def getEmptyNeighbors(self):
        empty = []
        for n in self.getNeighbors():
            if (n[0].getValue() == " "):
                empty.append(n)
        return empty

    