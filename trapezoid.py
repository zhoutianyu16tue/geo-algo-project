class Trapezoid(object):
        
    def __init__(self, leftPoint, rightPoint, top, bottom):
        self.leftPoint = leftPoint
        self.rightPoint = rightPoint
        self.top = top
        self.bottom = bottom
        self.upperLeft = None
        self.upperRight = None
        self.lowerLeft = None
        self.lowerRight = None
        self.inside = True
        self.sink = None
        self.key = hash(self)
        
    def updateLeft(self, ul, ll):
        self.upperLeft = ul
        if ul != None: ul.upperRight = self
        self.lowerLeft = ll
        if ll != None: ll.lowerRight = self
          
    def updateRight(self, ur, lr):
        self.upperRight = ur
        if ur != None: ur.upperLeft = self
        self.lowerRight = lr
        if lr != None: lr.lowerLeft = self 
          
    def updateLeftRight(self, ul, ll, ur, lr):
        self.upperLeft = ul
        if ul != None: ul.upperRight = self
        self.lowerLeft = ll
        if ll != None: ll.lowerRight = self
        self.upperRight = ur
        if ur != None: ur.upperLeft = self
        self.lowerRight = lr
        if lr != None: lr.lowerLeft = self  
         
    def trimNeighbors(self):
        if self.inside:
            self.inside = False
            if self.upperLeft != None: self.upperLeft.trimNeighbors()
            if self.lowerLeft != None: self.lowerLeft.trimNeighbors()
            if self.upperRight != None: self.upperRight.trimNeighbors()
            if self.lowerRight != None: self.lowerRight.trimNeighbors()
  
    def contains(self, point):
        return (point.x > self.leftPoint.x and point.x < self.rightPoint.x and 
                self.top.isAbove(point) and self.bottom.isBelow(point))
  
    def vertices(self):
        v1 = lineIntersection(self.top, self.leftPoint.x)
        v2 = lineIntersection(self.bottom, self.leftPoint.x)
        v3 = lineIntersection(self.bottom, self.rightPoint.x)
        v4 = lineIntersection(self.top, self.rightPoint.x)
        return v1, v2, v3, v4
  
    def addPoints(self):
        if self.leftPoint is not self.bottom.p: 
            self.bottom.addMPoint(self.leftPoint)
        if self.rightPoint is not self.bottom.q: 
            self.bottom.addMPoint(self.rightPoint)
        if self.leftPoint is not self.top.p: 
            self.top.addMPoint(self.leftPoint)
        if self.rightPoint is not self.top.q: 
            self.top.addMPoint(self.rightPoint)

def lineIntersection(edge, x):
    y =  edge.slope * x + edge.b
    return x, y