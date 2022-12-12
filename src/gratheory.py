#graph

#vertices are labelled 0-(n-1), pass this as an integer n

#edges is a list of lists length 3 containing the starting vertices, the ending vertices and the weights, use weight of 1 for unweighted graphs

#connectFrom and connectTo both specify where any connections come from or to and their weights as a list of lists length 2

#find shortest path finds the shortest path between two vertices (passed through as parameters) and returns a list 
#of vertices which are the shortest path followed by its weight in a tuple 
from queue import Queue, PriorityQueue
from collections import defaultdict


class inf:
    
    def __eq__(self, o):
        return False
    
    def __lt__(self, o):
        return False
    
    def __gt__(self, o):
        return True
    
    def __add__(self, o):
        return self
    
    def __sub__(self, o):
        return self
    
    def __rsub__(self, o):
        return self
    
    def __radd__(self,o):
        return self
        

class Vertex:
    def __init__(self,n):
        self.connectTo = []
        self.connectFrom = []
        self.number = n
    
class Graph:
    def __init__(self,edges,oneWayEdges=True):
        self.vertices = []
        self.length = 0
        self.oneWay = oneWayEdges
        self.edges = edges
        self.namesToNumbers = {}
        self.numbersToNames = {}
        
        for i in edges:
            if i[0] not in self.namesToNumbers.keys():
                self.addVertex(i[0])
            if i[1] not in self.namesToNumbers.keys():
                self.addVertex(i[1])
            
            self.addEdge(i)
            
    def findShortestPath(self,start,end,searchType = 'Ford', raiseError=False):
        if not (start in self.namesToNumbers.keys() and end in self.namesToNumbers.keys()):
            if raiseError:
                raise Exception("Start or end not in graph")
            else:
                return None, None
        if end not in self.BFS(start):
            if raiseError:
                raise Exception('Path does not exist')
            else:
                return None, None
        
        if searchType == 'Ford':
            if not (start in self.namesToNumbers.keys() and end in self.namesToNumbers.keys()):
                raise Exception("Start or end not in graph")
            start = self.namesToNumbers[start]
            end = self.namesToNumbers[end]
            vertices = [[i,inf()] for i in range(self.length)]
            vertices[start] = [0,0]
            changes = 1
            while changes != 0:
                changes = 0
                for i in range(self.length):
                    for j in self.vertices[i].connectFrom:
                        if vertices[i][1] > (vertices[j[0]][1]+j[1]) and not isinstance(vertices[j[0]][1], inf):
                            vertices[i][1] = (vertices[j[0]][1]+j[1])
                            changes += 1

            currentPoint = end
            path = [end]
            count = 0
            while currentPoint != start and count <= self.length:
                for i in self.vertices[currentPoint].connectFrom:
                    if i[1] == (vertices[currentPoint][1] - vertices[i[0]][1]):
                        path.append(i[0])
                        currentPoint = i[0]
                        break
                count += 1

            else:
                path = [self.numbersToNames[i] for i in path[::-1]]
                return path, vertices[end][1]
            
            
        if searchType == 'Djikstra':
            start = self.namesToNumbers[start]
            end = self.namesToNumbers[end]
            
            queue = PriorityQueue()
            queue.put((0, start))
            visited = defaultdict(lambda :inf())
            currentNode = start
            while not queue.empty() and currentNode != end:
                dist, currentNode = queue.get()
                neighbours = self.vertices[currentNode].connectTo
                visited[currentNode] = dist
                for i in neighbours:
                    if i[0] not in visited.keys():
                        queue.put((dist+i[1], i[0]))
                        visited[i[0]] = dist+i[1]
            path = [end]
            while currentNode != start:
                for i in self.vertices[currentNode].connectFrom:
                    if i[1] == visited[currentNode] - visited[i[0]]:
                        path.append(i[0])
                        currentNode = i[0]
            return [self.numbersToNames[i] for i in path[::-1]], visited[end]
    
    def DFS(self, vertex, reverseEdges=False):
        stack = [self.namesToNumbers[vertex]]
        visited = []
        while stack != []:
            nextNode = stack.pop()
            if nextNode not in visited:
                visited.append(nextNode)
                if reverseEdges:
                    connects = self.vertices[nextNode].connectFrom
                else:
                    connects = self.vertices[nextNode].connectTo
                for i in connects:
                    stack.append(i[0])
                    
        return [self.numbersToNames[i] for i in visited]
                
    def BFS(self, vertex, reverseEdges=False):
        queue = Queue()
        queue.put(self.namesToNumbers[vertex])
        visited = []
        while not queue.empty():
            nextNode = queue.get()
            if nextNode not in visited:
                visited.append(nextNode)
                if reverseEdges:
                    connects = self.vertices[nextNode].connectFrom
                else:
                    connects = self.vertices[nextNode].connectTo
                for i in connects:
                    queue.put(i[0])
        
        return [self.numbersToNames[i] for i in visited]
    
    def addVertex(self, v, raiseError = True):
        if v in self.namesToNumbers.keys():
            if raiseError:
                raise Exception("Vertex already exists")
            return self.namesToNumbers[v]
        else:
            self.vertices.append(Vertex(self.length))
            self.namesToNumbers[v] = self.length
            self.numbersToNames[self.length] = v
            self.length += 1
            return (self.length-1)
    
    def addEdge(self, e, oneWay=True , raiseError = True):
        if e[0] not in self.namesToNumbers.keys():
            if raiseError:
                raise Exception("First node not in graph")
            self.addVertex(e[0])
        if e[1] not in self.namesToNumbers.keys():
            if raiseError:
                raise Exception("Second node not in graph")
            self.addVertex(e[1])
        if oneWay and not self.oneWay:
            oneWay = self.oneWay 
        
        self.vertices[self.namesToNumbers[e[0]]].connectTo.append([self.namesToNumbers[e[1]], e[2]])
        self.vertices[self.namesToNumbers[e[1]]].connectFrom.append([self.namesToNumbers[e[0]], e[2]])
        if not oneWay:
            self.vertices[self.namesToNumbers[e[1]]].connectTo.append([self.namesToNumbers[e[0]], e[2]])
            self.vertices[self.namesToNumbers[e[0]]].connectFrom.append([self.namesToNumbers[e[1]], e[2]])
