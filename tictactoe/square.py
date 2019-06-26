class Square:

    def __init__(self, location):
        self.value = ""
        self.location = location

    def setValue(self, newValue):
        self.value = newValue

    def getValue(self):
        return self.value

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors

    def getNeighbors(self):
        return self.neighbors

    def getMatchingNeighbors(self):
        matchingNeighbors = []
        for n in getNeighbors():
            if n.getValue() == self.value:
                matchingNeighbors.append(n)
        return matchingNeighbors

    