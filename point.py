class Point():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isAbove(self, edge):
        return self.crossProduct(edge) > 0
        
    def isBelow(self, edge):
        return self.crossProduct(edge) < 0

    def crossProduct(self, edge):
        cpx = self.x - edge.p.x
        cpy = self.y - edge.p.y
        cqx = self.x - edge.q.x
        cqy = self.y - edge.q.y
        return cpx * cqy - cpy * cqx
