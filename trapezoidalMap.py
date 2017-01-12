from point import Point
from edge import Edge
from trapezoid import Trapezoid
import sys

class TrapezoidalMap():

    def __init__(self, boundingBox):
        self.map = {}
        self.bcross = None
        self.tcross = None
        self.map[boundingBox.hashCode] = boundingBox
        
    def trapezoidContainEdge(self, trapezoid, edge):
        A = Trapezoid(trapezoid.leftPoint, edge.p, trapezoid.top, trapezoid.bottom)
        B = Trapezoid(edge.p, edge.q, trapezoid.top, edge)
        C = Trapezoid(edge.p, edge.q, edge, trapezoid.bottom)
        D = Trapezoid(edge.q, trapezoid.rightPoint, trapezoid.top, trapezoid.bottom)

        A.updateLeft(trapezoid.upperLeft, trapezoid.lowerLeft)
        B.updateLeftRight(A, None, D, None)
        C.updateLeftRight(None, A, None, D)
        D.updateRight(trapezoid.upperRight, trapezoid.lowerRight)
        return [A, B, C, D]

    def trapezoidContainLeftEndpint(self, trapezoid, edge):
        rp = edge.q if edge.q.x == trapezoid.rightPoint.x else trapezoid.rightPoint

        A = Trapezoid(trapezoid.leftPoint, edge.p, trapezoid.top, trapezoid.bottom)
        B = Trapezoid(edge.p, rp, trapezoid.top, edge)
        C = Trapezoid(edge.p, rp, edge, trapezoid.bottom)
        A.updateLeft(trapezoid.upperLeft, trapezoid.lowerLeft)
        B.updateLeftRight(A, None, trapezoid.upperRight, None)
        C.updateLeftRight(None, A, None, trapezoid.lowerRight)

        self.bcross = trapezoid.bottom
        self.tcross = trapezoid.top
        edge.above = B
        edge.below = C
        return [A, B, C]
  
    def trapezoidCrossedByEdge(self, trapezoid, edge):
        lp = edge.p if edge.p.x == trapezoid.leftPoint.x  else trapezoid.leftPoint
        rp = edge.q if edge.q.x == trapezoid.rightPoint.x else trapezoid.rightPoint

        if self.tcross is trapezoid.top:
            A = trapezoid.upperLeft
            A.updateRight(trapezoid.upperRight, None)
            A.rightPoint = rp
        else:
            A = Trapezoid(lp, rp, trapezoid.top, edge)
            A.updateLeftRight(trapezoid.upperLeft, edge.above, trapezoid.upperRight, None)

        if self.bcross is trapezoid.bottom:
            B = trapezoid.lowerLeft
            B.updateRight(None, trapezoid.lowerRight)
            B.rightPoint = rp
        else:
            B = Trapezoid(lp, rp, edge, trapezoid.bottom)
            B.updateLeftRight(edge.below, trapezoid.lowerLeft, None, trapezoid.lowerRight)

        self.bcross = trapezoid.bottom
        self.tcross = trapezoid.top
        edge.above = A
        edge.below = B
        return [A, B]

    def trapezoidContainRightEndpint(self, trapezoid, edge):
        lp = edge.p if edge.p.x == trapezoid.leftPoint.x else trapezoid.leftPoint

        if self.tcross is trapezoid.top:
            A = trapezoid.upperLeft
            A.rightPoint = edge.q
        else:
            A = Trapezoid(lp, edge.q, trapezoid.top, edge)
            A.updateLeft(trapezoid.upperLeft, edge.above)

        if self.bcross is trapezoid.bottom:
            B = trapezoid.lowerLeft
            B.rightPoint = edge.q
        else:
            B = Trapezoid(lp, edge.q, edge, trapezoid.bottom)
            B.updateLeft(edge.below, trapezoid.lowerLeft)

        C = Trapezoid(edge.q, trapezoid.rightPoint, trapezoid.top, trapezoid.bottom)
        C.updateLeftRight(A, B, trapezoid.upperRight, trapezoid.lowerRight)
        return [A, B, C]
