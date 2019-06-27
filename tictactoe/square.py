class Square:

    def __init__(self, location):
        self.value = " "
        self.location = location

    def setValue(self, newValue):
        self.value = newValue

    def getValue(self):
        return self.value

    def getLocation(self):
        return self.location

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors

    def getNeighbors(self):
        return self.neighbors

    def getMatchingNeighbors(self):
        matchingNeighbors = []
        for n in self.getNeighbors():
            if n[0].getValue() == self.value:
                matchingNeighbors.append(n)
        return matchingNeighbors

    