PyGraph - A mathematical graphing module for python

Create a graph - 

from PyGraph import graph

g = graph(l, oneWayEdges = k)

where l is a list of edges in the format of [A, B, C] is an edge from A to B with weighting of C and oneWayEdges is a boolean of whether edges go in both directions or not.

To find the shortest path, use g.findShortestPath(start, end, searchType = A) where start is the start vertex, end is the end vertex and searchType is either 'Ford' or 'Djikstra' deciding which algorithm to implement, the default being 'Ford'.

Depth first search and Breadth first search will soon be implemented as DFS and BFS.
