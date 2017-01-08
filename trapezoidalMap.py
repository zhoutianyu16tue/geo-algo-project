from point import Point
from edge import Edge
from trapezoid import Trapezoid
import sys

class TrapezoidalMap():

    def __init__(self):
        self.map = {}
        self.bcross = None
        self.tcross = None
        # make the bounding box as the initial trapezoid
        maxX = sys.maxsize
        maxY = maxX
        minX = -sys.maxsize + 1
        minY = minX
        top = Edge(Point(minX, maxY), Point(maxX, maxY))
        bottom = Edge(Point(minX, minY), Point(maxX, minY))
        left = Point(minX, maxY)
        right = Point(maxX, maxY)
        self.boundingBox = Trapezoid(left, right, top, bottom)
        self.map[self.boundingBox.key] = self.boundingBox

    def clear(self):
        self.bcross = None
        self.tcross = None
        
    def case1(self, t, e):
        trapezoids = []
        trapezoids.append(Trapezoid(t.leftPoint, e.p, t.top, t.bottom))
        trapezoids.append(Trapezoid(e.p, e.q, t.top, e))
        trapezoids.append(Trapezoid(e.p, e.q, e, t.bottom))
        trapezoids.append(Trapezoid(e.q, t.rightPoint, t.top, t.bottom))
        trapezoids[0].updateLeft(t.upperLeft, t.lowerLeft)
        trapezoids[1].updateLeftRight(trapezoids[0], None, trapezoids[3], None)
        trapezoids[2].updateLeftRight(None, trapezoids[0], None, trapezoids[3])
        trapezoids[3].updateRight(t.upperRight, t.lowerRight)
        return trapezoids

    def case2(self, t, e):
        rp = e.q if e.q.x == t.rightPoint.x else t.rightPoint
        trapezoids = []
        trapezoids.append(Trapezoid(t.leftPoint, e.p, t.top, t.bottom))
        trapezoids.append(Trapezoid(e.p, rp, t.top, e))
        trapezoids.append(Trapezoid(e.p, rp, e, t.bottom))
        trapezoids[0].updateLeft(t.upperLeft, t.lowerLeft)
        trapezoids[1].updateLeftRight(trapezoids[0], None, t.upperRight, None)
        trapezoids[2].updateLeftRight(None, trapezoids[0], None, t.lowerRight)
        self.bcross = t.bottom
        self.tcross = t.top
        e.above = trapezoids[1]
        e.below = trapezoids[2]
        return trapezoids
  
    def case3(self, t, e):
        lp = e.p if e.p.x == t.leftPoint.x  else t.leftPoint
        rp = e.q if e.q.x == t.rightPoint.x else t.rightPoint
        trapezoids = []
        if self.tcross is t.top:
            trapezoids.append(t.upperLeft)
            trapezoids[0].updateRight(t.upperRight, None)
            trapezoids[0].rightPoint = rp
        else:
            trapezoids.append(Trapezoid(lp, rp, t.top, e))
            trapezoids[0].updateLeftRight(t.upperLeft, e.above, t.upperRight, None)
        if self.bcross is t.bottom:
            trapezoids.append(t.lowerLeft)
            trapezoids[1].updateRight(None, t.lowerRight)
            trapezoids[1].rightPoint = rp
        else:
            trapezoids.append(Trapezoid(lp, rp, e, t.bottom))
            trapezoids[1].updateLeftRight(e.below, t.lowerLeft, None, t.lowerRight)
        self.bcross = t.bottom
        self.tcross = t.top
        e.above = trapezoids[0]
        e.below = trapezoids[1]
        return trapezoids

    def case4(self, t, e):
        lp = e.p if e.p.x == t.leftPoint.x else t.leftPoint
        trapezoids = []
        if self.tcross is t.top:
            trapezoids.append(t.upperLeft)
            trapezoids[0].rightPoint = e.q
        else:
            trapezoids.append(Trapezoid(lp, e.q, t.top, e))
            trapezoids[0].updateLeft(t.upperLeft, e.above)
        if self.bcross is t.bottom:
            trapezoids.append(t.lowerLeft)
            trapezoids[1].rightPoint = e.q
        else:
            trapezoids.append(Trapezoid(lp, e.q, e, t.bottom))
            trapezoids[1].updateLeft(e.below, t.lowerLeft)
        trapezoids.append(Trapezoid(e.q, t.rightPoint, t.top, t.bottom))
        trapezoids[2].updateLeftRight(trapezoids[0], trapezoids[1], t.upperRight, t.lowerRight)
        return trapezoids
