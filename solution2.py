'''
Find a way to display every node in a tree without causing overlapping leaves.
Show the nodes in a grid. I.e., give each node a pair of coordinates (x, y) showing
where in the grid those nodes should appear. Every parent node should be directly
above or above and in between child nodes. The root node has a y-coordinate of 0,
and the farthest-left node has an x-coordinate of 0. Every child is one y-coordinate
below its parent.

SOLUTION 2

This solution is similar to solution 1, but we can remove the step where we
pre-compute widths. Here we ensure that each leaf has a different x-coordinate.
If each leaf has a different x-coordinate, intermediate nodes will not overlap
either because they are assigned to be in the middle of their leaves.

Use the following tree as an example:
    A
  B   C
D E F G

To compute y-coordinates, we set each node's y-coordinate to be one more than
its parent using a simple recursive DFS.
Tree of y-coordinates:
    0
  1   1
2 2 2 2

To compute x-coordinates, use our "minX" variable to keep track of the left-most
coordinate a subtree can place a node. This is the same as the minX variable in
Solution 1, but we will compute it differently.
Tree of minX (left-most coordinate of a sub-tree):
    0
  0   3
0 1 2 3

Note that every leaf has a different x-coordinate, which is the same as its
value for minX. In our recursive DFS, we initially pass a 0 in for minX and
increment it each time we hit a leaf. Rather than store this value as a
global or class variable, we can just return the result of our increment, and
the parent can pass the incremented value into its next child.
Tree of x-coordinates set for leaves:
    ?
  ?   ?
0 1 2 3

We also need to know what each intermediate node should return. Basically, each
node needs to tell its parent the left-most coordinate where the next sub-tree
is allowed to be placed. For a leaf, this is minX+1, but for intermediate
nodes, we can return whatever its right-most child returned.
Tree of nextMinX (what each node returns):
    4
  3   4
1 2 3 4

At this point, we have assigned x-coordinates to every leaf, and every
intermediate node knows its left-most coordinate (minX) and its right-most
coordinate (nextMinX, the value its right-most child returned). Intermediate
nodes can be placed in the exact center of minX and nextMinX using an average.
x = (minX + nextMinX) // 2
Tree of x-coordinates:
    2
  1   3
0 1 2 3
'''

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.x = None
        self.y = None

    def addChild(self, child):
        self.children.append(child)

    # Computes x-coordinates at each node.
    # minX = the farthest-left position the first leaf node under this can be placed.
    # Returns the farthest-left position the next leaf node can be placed.
    def computeX(self, minX = 0):
        if len(self.children) == 0:
            self.x = minX
            return self.x + 1

        nextMinX = minX
        for child in self.children:
            nextMinX = child.computeX(nextMinX)

        self.x = (minX + nextMinX) // 2
        return nextMinX

    def computeY(self, level = 0):
        self.y = level

        for child in self.children:
            child.computeY(level + 1)

    def gatherNodes(self, nodeList):
        nodeList.append(self)

        for child in self.children:
            child.gatherNodes(nodeList)

def computeCoordinates(rootNode):
    rootNode.computeX()
    rootNode.computeY()

def printTree(rootNode):
    nodeList = []
    rootNode.gatherNodes(nodeList)

    maxX = 0
    maxY = 0
    for node in nodeList:
        if node.x > maxX:
            maxX = node.x
        if node.y > maxY:
            maxY = node.y
    
    grid = [[None for x in range(maxX + 1)] for y in range(maxY + 1)]
    for node in nodeList:
        grid[node.y][node.x] = node.name
    
    s = ""
    for row in grid:
        for cell in row:
            s += ("." if cell == None else cell) + " "
        s += "\n"

    print(s)

def test1():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    
    a.addChild(b)
    a.addChild(c)

    computeCoordinates(a)
    printTree(a)

    assert a.x == 1
    assert a.y == 0
    assert b.x == 0
    assert b.y == 1
    assert c.x == 1
    assert c.y == 1

def test2():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")
    f = Node("F")
    
    a.addChild(b)
    a.addChild(c)
    b.addChild(d)
    b.addChild(e)
    c.addChild(f)

    computeCoordinates(a)
    printTree(a)

    assert a.x == 1
    assert a.y == 0
    assert b.x == 1
    assert b.y == 1
    assert c.x == 2
    assert c.y == 1
    assert d.x == 0
    assert d.y == 2
    assert e.x == 1
    assert e.y == 2
    assert f.x == 2
    assert f.y == 2

def test3():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")
    f = Node("F")
    g = Node("G")
    
    a.addChild(b)
    a.addChild(c)
    b.addChild(d)
    b.addChild(e)
    b.addChild(f)
    c.addChild(g)

    computeCoordinates(a)
    printTree(a)

    assert a.x == 2
    assert a.y == 0
    assert b.x == 1
    assert b.y == 1
    assert c.x == 3
    assert c.y == 1
    assert d.x == 0
    assert d.y == 2
    assert e.x == 1
    assert e.y == 2
    assert f.x == 2
    assert f.y == 2
    assert g.x == 3
    assert g.y == 2

def test4():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")
    f = Node("F")
    g = Node("G")
    
    a.addChild(b)
    a.addChild(c)
    a.addChild(d)
    c.addChild(e)
    e.addChild(f)
    f.addChild(g)

    computeCoordinates(a)
    printTree(a)

    assert a.x == 1
    assert a.y == 0
    assert b.x == 0
    assert b.y == 1
    assert c.x == 1
    assert c.y == 1
    assert d.x == 2
    assert d.y == 1
    assert e.x == 1
    assert e.y == 2
    assert f.x == 1
    assert f.y == 3
    assert g.x == 1
    assert g.y == 4

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()