from trapezoidalMap import TrapezoidalMap
from searchGraph import SearchGraph
from trapezoid import Trapezoid

class Trapezoidize():

    def __init__(self, edges, boundingBox):
        self.trapezoids = []
        self.edges = edges
        self.boundingBox = boundingBox
        self.trapezoidalMap = TrapezoidalMap(self.boundingBox)
        self.searchGraph = SearchGraph((self.boundingBox.node))
 
        self.trapezoidize()
    
    # Build the trapezoidal map and search graph
    def trapezoidize(self):
        for edge in self.edges:
            trapezoidsIntersected = self.searchGraph.followSegment(edge)

            for trapezoid in trapezoidsIntersected:

                self.trapezoidalMap.map.pop(trapezoid.hashCode, None)

                pInside = edge.p.inside(trapezoid)
                qInside = edge.q.inside(trapezoid)

                if pInside and qInside:
                    newTrapezoids = self.trapezoidalMap.trapezoidContainEdge(trapezoid, edge)
                    self.searchGraph.trapezoidContainEdge(trapezoid.node, edge, newTrapezoids)
                elif pInside and not qInside:
                    newTrapezoids = self.trapezoidalMap.trapezoidContainLeftEndpint(trapezoid, edge) 
                    self.searchGraph.trapezoidContainLeftEndpint(trapezoid.node, edge, newTrapezoids)
                elif not pInside and not qInside:
                    newTrapezoids = self.trapezoidalMap.trapezoidCrossedByEdge(trapezoid, edge)
                    self.searchGraph.trapezoidCrossedByEdge(trapezoid.node, edge, newTrapezoids)
                else:
                    newTrapezoids = self.trapezoidalMap.trapezoidContainRightEndpint(trapezoid, edge)
                    self.searchGraph.trapezoidContainRightEndpint(trapezoid.node, edge, newTrapezoids)

                for t in newTrapezoids:
                    self.trapezoidalMap.map[t.hashCode] = t

            self.trapezoidalMap.bcross = None
            self.trapezoidalMap.tcross = None                    

        for trapezoid in self.trapezoidalMap.map.values():
            if not (trapezoid.top is self.boundingBox.top or trapezoid.bottom is self.boundingBox.bottom):
                self.trapezoids.append(trapezoid)
