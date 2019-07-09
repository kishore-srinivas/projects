from binaryTree import BinaryTree
from binaryTree import Node

data = [7, 4, 5, 2, 6, 1, 3]

tree = BinaryTree()
for x in data:
    tree.addNode(Node(x))
tree.organizeTree()
tree.printTree()
print(tree.find(1))
print(tree.find(2))
print(tree.find(5))
print(tree.find(8))