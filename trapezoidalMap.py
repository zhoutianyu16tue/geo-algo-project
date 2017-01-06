from point import Point
from edge import Edge
from trapezoid import Trapezoid

class TrapezoidalMap():

    def __init__(self):
        self.map = {}
        self.margin = 50.0
        self.bcross = None
        self.tcross = None

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
  
    def boundingBox(self, edges): 
        margin = self.margin
        max = edges[0].p + margin
        min = edges[0].q - margin
        for e in edges:
            if e.p.x > max.x: max = Point(e.p.x + margin, max.y)
            if e.p.y > max.y: max = Point(max.x, e.p.y + margin)
            if e.q.x > max.x: max = Point(e.q.x + margin, max.y)
            if e.q.y > max.y: max = Point(max.x, e.q.y + margin)
            if e.p.x < min.x: min = Point(e.p.x - margin, min.y)
            if e.p.y < min.y: min = Point(min.x, e.p.y - margin)
            if e.q.x < min.x: min = Point(e.q.x - margin, min.y)
            if e.q.y < min.y: min = Point(min.x, e.q.y - margin)
        top = Edge(Point(min.x, max.y), Point(max.x, max.y))
        bottom = Edge(Point(min.x, min.y), Point(max.x, min.y))
        left = top.p
        right = top.q
        trap = Trapezoid(left, right, top, bottom)
        self.map[trap.key] = trap
        return trap