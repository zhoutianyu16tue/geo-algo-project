from searchGraph import LeafNode

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
        self.node = LeafNode(self)
        self.hashCode = hash(self)
        
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
  
    def vertices(self):
        v1 = lineIntersection(self.top, self.leftPoint.x)
        v2 = lineIntersection(self.bottom, self.leftPoint.x)
        v3 = lineIntersection(self.bottom, self.rightPoint.x)
        v4 = lineIntersection(self.top, self.rightPoint.x)
        return (v1, v2, v3, v4)

def lineIntersection(edge, x):
    y =  edge.slope * x + edge.b
    return x, y