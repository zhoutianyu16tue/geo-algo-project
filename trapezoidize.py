from trapezoidalMap import TrapezoidalMap
from searchGraph import SearchGraph
from trapezoid import Trapezoid
from datetime import datetime
from math import ceil, log2

class Trapezoidize():

    def __init__(self, edges, boundingBox):
        self.trapezoids = []
        self.edges = edges
        self.boundingBox = boundingBox
        self.trapezoidalMap = TrapezoidalMap(self.boundingBox)
        self.searchGraph = SearchGraph((self.boundingBox.node))
        
        self.startingFromRoot = 0
        before = datetime.now()
        # self.trapezoidize()
        self.seidel()
        after = datetime.now()
        time = after - before
        # print('%f ms' % (time.total_seconds() * 1000))
        self.runningTime = (time.total_seconds() * 1000)

    def seidel(self):
        # handle the 1st edge
        t = self.searchGraph.find(self.searchGraph.root, self.edges[0])
        self.trapezoidalMap.map.pop(t.trapezoid.hashCode, None)
        newTrapezoids = self.trapezoidalMap.trapezoidContainEdge(t.trapezoid, self.edges[0])
        # print('newTrapezoids %d' % len(newTrapezoids))
        self.searchGraph.trapezoidContainEdge(t.trapezoid.node, self.edges[0], newTrapezoids)

        h = 1
        n = len(self.edges)
        i = 0
        while h <= H(n):
            # print('h: %d' % h)
            i = N(n, h - 1)

            while i < N(n, h):
                # print('i: %d' % i)
                if len(self.edges[i].parentList) == 0:
                    # print('Starting from root')
                    self.startingFromRoot += 1
                    startingNode = self.searchGraph.root
                elif self.edges[i].left is True:
                    startingNode = self.edges[i].parentList[0].left
                else:
                    startingNode = self.edges[i].parentList[0].right

                self.handleEdge(startingNode, self.edges[i])
                i += 1

            for edge in self.edges[N(n, h):]:
                node = self.searchGraph.find(self.searchGraph.root, edge)
                edge.parentList = node.parentList
                if node.parentList:
                        edge.left = True if node.parentList[0].left is node else False
            h += 1

        # print('here')
        while i < n:
            # print('i: %d' % i)
            if len(self.edges[i].parentList) == 0:
                    # print('Starting from root')
                self.startingFromRoot += 1
                startingNode = self.searchGraph.root
            elif self.edges[i].left is True:
                startingNode = self.edges[i].parentList[0].left
            else:
                startingNode = self.edges[i].parentList[0].right
                    
            self.handleEdge(startingNode, self.edges[i])
            i += 1

        # for trapezoid in self.trapezoidalMap.map.values():
        #     if not (trapezoid.top is self.boundingBox.top or trapezoid.bottom is self.boundingBox.bottom):
        #         self.trapezoids.append(trapezoid)
                
        # for t in self.trapezoidalMap.map.values():
        #     if t.top is self.boundingBox.top or t.bottom is self.boundingBox.bottom:
        #         t.trimNeighbors()
            
        # # Collect interior trapezoids
        # for t in self.trapezoidalMap.map.values():
        #     if t.inside:
        #         self.trapezoids.append(t)

    # Build the trapezoidal map and search graph
    def trapezoidize(self):
        for edge in self.edges:
            self.handleEdge(self.searchGraph.root, edge)

        # the bounding box has the size of infinity,
        # which cannot be drawn and must be removed.
        # This can be commented when testing
        # for trapezoid in self.trapezoidalMap.map.values():
        #     if not (trapezoid.top is self.boundingBox.top or trapezoid.bottom is self.boundingBox.bottom):
        #         self.trapezoids.append(trapezoid)

    def handleEdge(self, startingNode, edge):
        trapezoidsIntersected = self.searchGraph.followSegment(startingNode, edge)
        # print('len of trapezoidsIntersected: %d' % len(trapezoidsIntersected))
        # print(trapezoidsIntersected, '\n')
        self.handleIntersectedTrapezoids(trapezoidsIntersected, edge)
    
    def handleIntersectedTrapezoids(self, trapezoidsIntersected, edge):
        for trapezoid in trapezoidsIntersected:
            if trapezoid is None:
                continue

            self.trapezoidalMap.map.pop(trapezoid.hashCode, None)

            pInside = edge.p.inside(trapezoid)
            qInside = edge.q.inside(trapezoid)

            if pInside and qInside:
                # See picture trapezoidContainEdge.pdf
                newTrapezoids = self.trapezoidalMap.trapezoidContainEdge(trapezoid, edge)
                self.searchGraph.trapezoidContainEdge(trapezoid.node, edge, newTrapezoids)

            elif pInside and not qInside:
                # See picture trapezoidContainLeftEndpint.pdf
                newTrapezoids = self.trapezoidalMap.trapezoidContainLeftEndpint(trapezoid, edge) 
                self.searchGraph.trapezoidContainLeftEndpint(trapezoid.node, edge, newTrapezoids)

            elif not pInside and not qInside:
                # See picture trapezoidCrossedByEdge.pdf
                newTrapezoids = self.trapezoidalMap.trapezoidCrossedByEdge(trapezoid, edge)
                self.searchGraph.trapezoidCrossedByEdge(trapezoid.node, edge, newTrapezoids)

            else:
                # See picture trapezoidContainRightEndpint.pdf
                newTrapezoids = self.trapezoidalMap.trapezoidContainRightEndpint(trapezoid, edge)
                self.searchGraph.trapezoidContainRightEndpint(trapezoid.node, edge, newTrapezoids)

            for t in newTrapezoids:
                self.trapezoidalMap.map[t.hashCode] = t

        self.trapezoidalMap.bottom = None
        self.trapezoidalMap.top = None

def H(n):
    cnt = 0
    while n >= 1.0:
        cnt += 1
        n = log2(n)
    return cnt-1

def N(n, h):
    t = n
    while h > 0:
        t = log2(t)
        h -= 1
    return ceil(n/t)