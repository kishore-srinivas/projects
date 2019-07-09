class BinaryTree:
    def __init__(self):
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)

    def getDepth(self):
        total = 0
        n = 0
        while (total < len(self.nodes)):
            total = total + 2**n
            n = n + 1
        return n

    def getRootNode(self):
        return self.nodes[int(len(self.nodes)/2)]

    def organizeTree(self):
        print("root:", self.getRootNode().getValue())
        # depth = self.getDepth()        
        for n in self.nodes:
            current = self.getRootNode()
            if (n.getValue() == current.getValue()):
                continue
            placed = False
            while (placed == False):
                if (n.getValue() < current.getValue()):
                    if (current.getLeft() == None):
                        current.setLeft(n)
                        placed = True
                        continue
                    current = current.getLeft()
                if (n.getValue() > current.getValue()):
                    if (current.getRight() == None):
                        current.setRight(n)
                        placed = True
                        continue
                    current = current.getRight()

    def printTree(self):
        return self.getRootNode().printTree()   

    def find(self, value):
        path = []
        current = self.getRootNode()
        i = 0
        while (i < len(self.getAllNodes())):
            if (current is None):
                return ["not found"]
            if (value < current.getValue()):
                path.append("left")
                current = current.getLeft()
            elif (value > current.getValue()):
                path.append("right")
                current = current.getRight()
            else:
                break
            i = i + 1
        return path

    def getAllNodes(self):
        return self.nodes

class Node:
    def __init__(self, value, left=None, right=None):
        assert (type(value) == int), "VALUE expected an integer but was given: {}".format(value)
        self.value = value
        self.left = left
        self.right = right

    def setLeft(self, leftNode):
        self.left = leftNode

    def setRight(self, rightNode):
        self.right = rightNode
    
    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getValue(self):
        return self.value

    def printTree(self):
        if (self.getLeft()):
            self.getLeft().printTree()
        print(self.getValue())
        if (self.getRight()):
            self.getRight().printTree()
