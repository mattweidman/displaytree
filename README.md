# Display a tree in a grid

You want to write a program that displays nodes of a tree in a 2D grid, marked by non-negative
integer (x,y) coordinates. Given the root node of a tree, write a program to compute the (x,y)
coordinates of each node so that no two nodes overlap. Store these coordinates as fields in
each node object.

For example, the following tree:
````
    A
   / \
  B   C
/ | \ |
D E F G
````
would look like this in your grid:
````
    0 1 2 3
   ________
0 |     A   
1 |   B   C 
2 | D E F G 
````
with the following (x,y) coordinates:
````
A -> (2,0)
B -> (1,1)
C -> (3,1)
D -> (0,2)
E -> (1,2)
F -> (2,2)
G -> (3,2)
````

2 steps:

1. Compute y-coordinates of every node.
* The root node of your tree has a y-coordinate of 0.
* Y-coordinates increase as you go deeper in your tree.
* Every parent node is one coordinate above its children.

2. Compute x-coordinates of every node.
* The left-most node of your tree has an x-coordinate of 0.
* X-coordinates increase to the right.
* Every intermediate node is roughly horizontally centered among its descendants.
* If a node has an odd number of descendant leaves, it should be in their exact center.
Example:
````
  A
B C D
````
* If a node has an even number of descendant leaves, it can be on either side next to their center.
Example:
````
    A
B C D E
````