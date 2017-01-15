from trapezoidalMap import TrapezoidalMap
from searchGraph import SearchGraph
from trapezoid import Trapezoid
from datetime import datetime

class Trapezoidize():

    def __init__(self, edges, boundingBox):
        self.trapezoids = []
        self.edges = edges
        self.boundingBox = boundingBox
        self.trapezoidalMap = TrapezoidalMap(self.boundingBox)
        self.searchGraph = SearchGraph((self.boundingBox.node))
        
        before = datetime.now()
        self.trapezoidize()
        after = datetime.now()
        time = after - before
        # print('%f ms' % (time.total_seconds() * 1000))
        self.runningTime = (time.total_seconds() * 1000)
    # Build the trapezoidal map and search graph
    def trapezoidize(self):
        for edge in self.edges:
            trapezoidsIntersected = self.searchGraph.followSegment(edge)

            for trapezoid in trapezoidsIntersected:

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

        # the bounding box has the size of infinity,
        # which cannot be drawn and must be removed.
        # This can be commented when testing
        for trapezoid in self.trapezoidalMap.map.values():
            if not (trapezoid.top is self.boundingBox.top or trapezoid.bottom is self.boundingBox.bottom):
                self.trapezoids.append(trapezoid)
