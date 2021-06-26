'''
Find a way to display every node in a tree without causing overlapping leaves.
Show the nodes in a grid. I.e., give each node a pair of coordinates (x, y) showing
where in the grid those nodes should appear. Every parent node should be directly
above or above and in between child nodes. The root node has a y-coordinate of 0,
and the farthest-left node has an x-coordinate of 0. Every child is one y-coordinate
below its parent.

SOLUTION 1

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

To compute x-coordinates, we first compute the "width" of every node. The
width of a node is defined as the distance from the leftmost leaf below a node
to the rightmost leaf. A leaf node has a width of 1, and an intermediate node's
width is the sum of its children's widths. This lets us know the size of each
node's "territory," which lets us keep other sub-trees from overlapping. 
Tree of widths:
    4
  3   1
1 1 1 1

However, we still need to know where each territory exists horizontally, so the
left-most coordinate (minX) of each node's territory needs to be given. We know
that the left-most coordinate of the entire tree is 0, so we can pass in 0 for
minX in our initial call on the root. Each time a parent recurses over its
children, if figures out the width of the child it recursed over, adds its
width to minX, and passes that as minX to the next child.
Tree of minX (left-most coordinate of a sub-tree):
    0
  0   3
0 1 2 3

If we know minX and width, we can set each node's x-coordinate to be
x = minX + width // 2.
Tree of x-coordinates:
    2
  1   3
0 1 2 3
'''

import math

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.x = None
        self.y = None
        self.width = None
    
    def addChild(self, child):
        self.children.append(child)

    def computeWidth(self):
        if len(self.children) == 0:
            self.width = 1
        else:
            width = 0
            for child in self.children:
                width += child.computeWidth()
            self.width = width
        
        return self.width

    # computeWidth() must be called first
    def computeX(self, minX=0):
        self.x = math.floor(minX + self.width / 2)

        childMinX = minX
        for child in self.children:
            child.computeX(childMinX)
            childMinX += child.width

    def computeY(self, parentY=-1):
        self.y = parentY + 1
        for child in self.children:
            child.computeY(self.y)
        

def computeCoordinates(rootNode):
    rootNode.computeWidth()
    rootNode.computeX()
    rootNode.computeY()

def test1():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    
    a.addChild(b)
    a.addChild(c)

    computeCoordinates(a)

    assert a.width == 2
    assert b.width == 1
    assert c.width == 1
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

    assert a.width == 3
    assert b.width == 2
    assert c.width == 1
    assert d.width == 1
    assert e.width == 1
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

    assert a.width == 4
    assert b.width == 3
    assert c.width == 1
    assert d.width == 1
    assert e.width == 1
    assert f.width == 1
    assert g.width == 1
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