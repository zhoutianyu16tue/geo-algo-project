from point import Point
from edge import Edge
from random import shuffle, seed
from trapezoidalMap import TrapezoidalMap
from searchGraph import SearchGraph, isSink
from trapezoid import Trapezoid
import sys

Epsilon = 1e-5

class Trapezoidize():

    def __init__(self, points):
        self.trapezoids = []
        self.edges, self.boundingBox = self.connectPoints(points)
        self.trapezoidalMap = TrapezoidalMap(self.boundingBox)
        self.searchGraph = SearchGraph(isSink(self.boundingBox))
 
        self.trapezoidize()
    
    # Build the trapezoidal map and search graph
    def trapezoidize(self):
        for edge in self.edges:
            trapezoidsIntersected = self.searchGraph.followSegment(edge)

            for trapezoid in trapezoidsIntersected:

                self.trapezoidalMap.map.pop(trapezoid.key, None)

                # Bisect old trapezoids and create new
                cp = trapezoid.contains(edge.p)
                cq = trapezoid.contains(edge.q)
                if cp and cq:
                    tlist = self.trapezoidalMap.case1(trapezoid, edge)
                    self.searchGraph.case1(trapezoid.sink, edge, tlist)
                elif cp and not cq:
                    tlist = self.trapezoidalMap.case2(trapezoid, edge) 
                    self.searchGraph.case2(trapezoid.sink, edge, tlist)
                elif not cp and not cq:
                    tlist = self.trapezoidalMap.case3(trapezoid, edge)
                    self.searchGraph.case3(trapezoid.sink, edge, tlist)
                else:
                    tlist = self.trapezoidalMap.case4(trapezoid, edge)
                    self.searchGraph.case4(trapezoid.sink, edge, tlist)
                # Add new trapezoids to map
                for t in tlist:
                    self.trapezoidalMap.map[t.key] = t

            self.trapezoidalMap.bcross = None
            self.trapezoidalMap.tcross = None                    
        # Mark outside trapezoids w/ depth-first search
        for trapezoid in self.trapezoidalMap.map.values():
            self.markOutside(trapezoid)
            
        # Collect interior trapezoids
        for trapezoid in self.trapezoidalMap.map.values():
            if trapezoid.inside:
                self.trapezoids.append(trapezoid)
                trapezoid.addPoints()
               
  
    def markOutside(self, t):
        if t.top is self.boundingBox.top or t.bottom is self.boundingBox.bottom:
            t.trimNeighbors()
  
    def connectPoints(self, points):
        edgeList = []
        numberOfPoints = len(points)
        for idx, point in enumerate(points):
            next = idx + 1 if idx < numberOfPoints-1 else 0
            p = points[idx][0], points[idx][1]
            q = points[next][0], points[next][1]

            # if p[0] == q[0]:
            #     sys.exit('Detect vertical edge!')

            edgeList.append((p, q))

        maxX = sys.maxsize
        maxY = maxX
        minX = -sys.maxsize + 1
        minY = minX
        top = Edge(Point(minX, maxY), Point(maxX, maxY))
        bottom = Edge(Point(minX, minY), Point(maxX, minY))
        left = Point(minX, maxY)
        right = Point(maxX, maxY)

        return self.makeRandomOrderEdges(edgeList), Trapezoid(left, right, top, bottom)
  
    def makeRandomOrderEdges(self, edgeList):
        edges = []
        for e in edgeList:
            # p = Point(e[0][0], e[0][1])
            # q = Point(e[1][0], e[1][1])
            p = self.shearTransformation(e[0])
            q = self.shearTransformation(e[1])

            if p.x > q.x:
                edges.append(Edge(q, p))
            else:
                edges.append(Edge(p, q))
        
        seed()
        shuffle(edges)
        return edges

    def shearTransformation(self, point):
        return Point(point[0] + Epsilon * point[1], point[1])
