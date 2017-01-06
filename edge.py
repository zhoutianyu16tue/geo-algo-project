class Edge(object):
    
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.slope = (q.y - p.y) / (q.x - p.x) if q.x - p.x != 0 else 0
        self.b = p.y - (p.x * self.slope)
        self.above, self.below = None, None
        self.mpoints = [p, q]
    
    def isAbove(self, point):
        return orient2d(self.p, self.q, point) < 0
        
    def isBelow(self, point):
        return orient2d(self.p, self.q, point) > 0
        
    def addMPoint(self, point):
        for mp in self.mpoints:
            if mp.x == point.x and mp.y == point.y:
                return
        self.mpoints.append(point)

def orient2d(pa, pb, pc):
    acx = pa.x - pc.x;
    bcx = pb.x - pc.x;
    acy = pa.y - pc.y;
    bcy = pb.y - pc.y;
    return acx * bcy - acy * bcx;