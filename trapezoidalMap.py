from point import Point
from edge import Edge
from trapezoid import Trapezoid
import sys

class TrapezoidalMap():

    def __init__(self, boundingBox):
        self.map = {}
        self.bcross = None
        self.tcross = None
        self.map[boundingBox.key] = boundingBox
        
    def trapezoidContainEdge(self, t, e):
        A = Trapezoid(t.leftPoint, e.p, t.top, t.bottom)
        B = Trapezoid(e.p, e.q, t.top, e)
        C = Trapezoid(e.p, e.q, e, t.bottom)
        D = Trapezoid(e.q, t.rightPoint, t.top, t.bottom)

        A.updateLeft(t.upperLeft, t.lowerLeft)
        B.updateLeftRight(A, None, D, None)
        C.updateLeftRight(None, A, None, D)
        D.updateRight(t.upperRight, t.lowerRight)
        return [A, B, C, D]

    def trapezoidContainLeftEndpint(self, t, e):
        rp = e.q if e.q.x == t.rightPoint.x else t.rightPoint

        A = Trapezoid(t.leftPoint, e.p, t.top, t.bottom)
        B = Trapezoid(e.p, rp, t.top, e)
        C = Trapezoid(e.p, rp, e, t.bottom)
        A.updateLeft(t.upperLeft, t.lowerLeft)
        B.updateLeftRight(A, None, t.upperRight, None)
        C.updateLeftRight(None, A, None, t.lowerRight)

        self.bcross = t.bottom
        self.tcross = t.top
        e.above = B
        e.below = C
        return [A, B, C]
  
    def trapezoidCrossedByEdge(self, t, e):
        lp = e.p if e.p.x == t.leftPoint.x  else t.leftPoint
        rp = e.q if e.q.x == t.rightPoint.x else t.rightPoint

        if self.tcross is t.top:
            A = t.upperLeft
            A.updateRight(t.upperRight, None)
            A.rightPoint = rp
        else:
            A = Trapezoid(lp, rp, t.top, e)
            A.updateLeftRight(t.upperLeft, e.above, t.upperRight, None)

        if self.bcross is t.bottom:
            B = t.lowerLeft
            B.updateRight(None, t.lowerRight)
            B.rightPoint = rp
        else:
            B = Trapezoid(lp, rp, e, t.bottom)
            B.updateLeftRight(e.below, t.lowerLeft, None, t.lowerRight)

        self.bcross = t.bottom
        self.tcross = t.top
        e.above = A
        e.below = B
        return [A, B]

    def trapezoidContainRightEndpint(self, t, e):
        lp = e.p if e.p.x == t.leftPoint.x else t.leftPoint

        if self.tcross is t.top:
            A = t.upperLeft
            A.rightPoint = e.q
        else:
            A = Trapezoid(lp, e.q, t.top, e)
            A.updateLeft(t.upperLeft, e.above)

        if self.bcross is t.bottom:
            B = t.lowerLeft
            B.rightPoint = e.q
        else:
            B = Trapezoid(lp, e.q, e, t.bottom)
            B.updateLeft(e.below, t.lowerLeft)

        C = Trapezoid(e.q, t.rightPoint, t.top, t.bottom)
        C.updateLeftRight(A, B, t.upperRight, t.lowerRight)
        return [A, B, C]
