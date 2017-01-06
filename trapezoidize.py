from point import Point
from edge import Edge
from random import shuffle
from trapezoidalMap import TrapezoidalMap
from searchGraph import SearchGraph, isSink

SHEAR = 1e-3

class Trapezoidize():
     
    ## 
    ## Number of points should be > 3
    ##
    def __init__(self, poly_line):
        self.trapezoids = []
        self.edgeList = self.initEdges(poly_line)
        self.trapezoidalMap = TrapezoidalMap()
        self.boundingBox = self.trapezoidalMap.boundingBox(self.edgeList)
        self.searchGraph = SearchGraph(isSink(self.boundingBox))
            
        self.process()
    
    # Build the trapezoidal map and query graph
    def process(self):
        for edge in self.edgeList:
            traps = self.searchGraph.followEdge(edge)  
            for t in traps:
                # Remove old trapezods
                del self.trapezoidalMap.map[t.key]
                # Bisect old trapezoids and create new
                cp = t.contains(edge.p)
                cq = t.contains(edge.q)
                if cp and cq:
                    tlist = self.trapezoidalMap.case1(t, edge)
                    self.searchGraph.case1(t.sink, edge, tlist)
                elif cp and not cq:
                    tlist = self.trapezoidalMap.case2(t, edge) 
                    self.searchGraph.case2(t.sink, edge, tlist)
                elif not cp and not cq:
                    tlist = self.trapezoidalMap.case3(t, edge)
                    self.searchGraph.case3(t.sink, edge, tlist)
                else:
                    tlist = self.trapezoidalMap.case4(t, edge)
                    self.searchGraph.case4(t.sink, edge, tlist)
                # Add new trapezoids to map
                for t in tlist:
                    self.trapezoidalMap.map[t.key] = t
            self.trapezoidalMap.clear()
                    
        # Mark outside trapezoids w/ depth-first search
        for k, t in self.trapezoidalMap.map.items():
            self.markOutside(t)
            
        # Collect interior trapezoids
        for k, t in self.trapezoidalMap.map.items():
            if t.inside:
                self.trapezoids.append(t)
                t.addPoints()
               
  
    def markOutside(self, t):
        if t.top is self.boundingBox.top or t.bottom is self.boundingBox.bottom:
            t.trimNeighbors()
  
    def initEdges(self, points):
        edgeList = []
        size = len(points)
        for i in range(size):
            j = i + 1 if i < size-1 else 0
            p = points[i][0], points[i][1]
            q = points[j][0], points[j][1]
            edgeList.append((p, q))
        return self.orderEdges(edgeList)
  
    def orderEdges(self, edgeList):
        edges = []
        for e in edgeList:
            p = shearTransform(e[0])
            q = shearTransform(e[1])
            if p.x > q.x: 
                edges.append(Edge(q, p))
            else: 
                edges.append(Edge(p, q))
        # Randomized incremental algorithm
        shuffle(edges)
        return edges

def shearTransform(point):
    return Point(point[0] + SHEAR * point[1], point[1])