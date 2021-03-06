class Edge():
    
    def __init__(self, p, q):

        # point p always has smaller x coordinate
        if q.x < p.x:
            self.p = q
            self.q = p
        else:
            self.p = p
            self.q = q

        # q.x != p.x guaranteed by shear transformation
        self.slope = (q.y - p.y) / (q.x - p.x) if q.x != p.x else 0
        self.b = p.y - (p.x * self.slope)
        self.above, self.below = None, None
        self.parentList = []
        self.left = None
    
    def isAbove(self, point):
        return self.crossProduct(point) < 0
        
    def isBelow(self, point):
        return self.crossProduct(point) > 0

    def crossProduct(self, point):
        cpx = self.p.x - point.x
        cpy = self.p.y - point.y
        cqx = self.q.x - point.x
        cqy = self.q.y - point.y
        return cpx * cqy - cpy * cqx