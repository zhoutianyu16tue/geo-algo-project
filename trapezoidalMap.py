from point import Point
from edge import Edge
from trapezoid import Trapezoid
import sys

class TrapezoidalMap():

    def __init__(self, boundingBox):
        self.map = {}
        self.map[boundingBox.hashCode] = boundingBox
        self.bottom = None
        self.top = None
        
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
        rightPoint = edge.q if edge.q.x == trapezoid.rightPoint.x else trapezoid.rightPoint

        A = Trapezoid(trapezoid.leftPoint, edge.p, trapezoid.top, trapezoid.bottom)
        B = Trapezoid(edge.p, rightPoint, trapezoid.top, edge)
        C = Trapezoid(edge.p, rightPoint, edge, trapezoid.bottom)
        A.updateLeft(trapezoid.upperLeft, trapezoid.lowerLeft)
        B.updateLeftRight(A, None, trapezoid.upperRight, None)
        C.updateLeftRight(None, A, None, trapezoid.lowerRight)

        self.bottom = trapezoid.bottom
        self.top = trapezoid.top
        edge.above = B
        edge.below = C
        return [A, B, C]
  
    def trapezoidCrossedByEdge(self, trapezoid, edge):
        leftPoint = edge.p if edge.p.x == trapezoid.leftPoint.x  else trapezoid.leftPoint
        rightPoint = edge.q if edge.q.x == trapezoid.rightPoint.x else trapezoid.rightPoint

        if self.top is trapezoid.top:
            A = trapezoid.upperLeft
            A.updateRight(trapezoid.upperRight, None)
            A.rightPoint = rightPoint
        else:
            A = Trapezoid(leftPoint, rightPoint, trapezoid.top, edge)
            A.updateLeftRight(trapezoid.upperLeft, edge.above, trapezoid.upperRight, None)

        if self.bottom is trapezoid.bottom:
            B = trapezoid.lowerLeft
            B.updateRight(None, trapezoid.lowerRight)
            B.rightPoint = rightPoint
        else:
            B = Trapezoid(leftPoint, rightPoint, edge, trapezoid.bottom)
            B.updateLeftRight(edge.below, trapezoid.lowerLeft, None, trapezoid.lowerRight)

        self.bottom = trapezoid.bottom
        self.top = trapezoid.top
        edge.above = A
        edge.below = B
        return [A, B]

    def trapezoidContainRightEndpint(self, trapezoid, edge):
        leftPoint = edge.p if edge.p.x == trapezoid.leftPoint.x else trapezoid.leftPoint

        if self.top is trapezoid.top:
            A = trapezoid.upperLeft
            A.rightPoint = edge.q
        else:
            A = Trapezoid(leftPoint, edge.q, trapezoid.top, edge)
            A.updateLeft(trapezoid.upperLeft, edge.above)

        if self.bottom is trapezoid.bottom:
            B = trapezoid.lowerLeft
            B.rightPoint = edge.q
        else:
            B = Trapezoid(leftPoint, edge.q, edge, trapezoid.bottom)
            B.updateLeft(edge.below, trapezoid.lowerLeft)

        C = Trapezoid(edge.q, trapezoid.rightPoint, trapezoid.top, trapezoid.bottom)
        C.updateLeftRight(A, B, trapezoid.upperRight, trapezoid.lowerRight)
        return [A, B, C]
