import fileinput
import math
from queue import PriorityQueue

#files = ('std_in.txt')
with fileinput.input(files = ('input.txt')) as f:
    p=0
    n=0
    e=0
    nodes=[]
    searchedRoutes=[] 
    edges=[]

    class Route:
        def __init__(self, start, end):
            self.start=start
            self.end=end

    class Edge:
        def __init__(self, p1, p2, length):
            self.p1=p1
            self.p2=p2
            self.length=length

    class Node:
        def __init__(self, x, y):
            self.x=x
            self.y=y
            self.neighbours=[]

        

    def calculateLength(p1, p2):
        return math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)


    p=int(f.readline().rstrip())
    n=int(f.readline().rstrip())
    e=int(f.readline().rstrip())

    f.readline()

    for i in range(p):
        attributes=f.readline().rstrip().split("\t")
        searchedRoutes.append(Route(int(attributes[0]), int(attributes[1])))

    f.readline()

    for i in range(n):
        attributes=f.readline().rstrip().split("\t")
        nodes.append(Node(int(attributes[0]), int(attributes[1])))

    f.readline()

    for i in range(e):
        attributes=f.readline().rstrip().split("\t")
        length=calculateLength(nodes[int(attributes[0])], nodes[int(attributes[1])])
        edges.append(Edge(int(attributes[0]), int(attributes[1]), length))

    f.readline()

    def setNeighbours(nodeIdx):
        for ei in edges:
            if(ei.p1==nodeIdx):
                nodes[nodeIdx].neighbours.append({'length': ei.length, 'nodeIdx': ei.p2})          
            elif(ei.p2==nodeIdx):
                nodes[nodeIdx].neighbours.append({'length': ei.length, 'nodeIdx': ei.p1})

    for i in range(len(nodes)):
        setNeighbours(i)

    def existsInQueue(value, queue):
        for x in queue:
            if x[1] == value:
                return True
        return False

        

    def A_star(start, goal):
        openSet=PriorityQueue()

        g = []
        g = [math.inf for i in range(len(nodes))]
        g[start]=0

        f = []
        f = [math.inf for i in range(len(nodes))]
        f[start]=calculateLength(nodes[start], nodes[goal])

        openSet.put((f[start], start))

        while not openSet.empty():            
            current=openSet.get()

            if current[1]==goal:
                return current[0]

            for neighbour in nodes[current[1]].neighbours:
                possible_g=g[current[1]] + neighbour['length'] 
                neighbourIdx=neighbour['nodeIdx']
                if(possible_g < g[neighbourIdx]):
                    g[neighbourIdx]=possible_g
                    f[neighbourIdx]= possible_g + calculateLength(nodes[neighbourIdx], nodes[goal])

                    #if not existsInQueue(neighbourIdx, openSet.queue):
                    #    openSet.put((f[neighbourIdx], neighbourIdx))
                    openSet.put((f[neighbourIdx], neighbourIdx))



        return math.inf    

    results=[]
    for r in searchedRoutes:
        shortestPath=A_star(r.start, r.end)

        results.append(shortestPath)
        
    for i in results:
        print("{:0.2f}".format(i), end = '\t')


