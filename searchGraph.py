class Node():

    def __init__(self, lchild, rchild):
        self.parentList = []
        self.lchild = lchild
        self.rchild = rchild
        if lchild != None: 
            lchild.parentList.append(self)
        if rchild != None: 
            rchild.parentList.append(self)
        
    def replace(self, node):
        for parent in node.parentList:
            if parent.lchild is node: 
                parent.lchild = self
            else: 
                parent.rchild = self 
        self.parentList += node.parentList

class LeafNode(Node):
        
    def __init__(self, trapezoid):
        super(LeafNode, self).__init__(None, None)
        self.trapezoid = trapezoid
        trapezoid.sink = self
        
    def locate(self, edge): 
        return self

class PointNode(Node):

    def __init__(self, point, lchild, rchild):
        super(PointNode, self).__init__(lchild, rchild)
        self.point = point
    
    def locate(self, edge): 
        if edge.p.x >= self.point.x: 
            return self.rchild.locate(edge)
        return self.lchild.locate(edge)

class EdgeNode(Node):
    
    def __init__(self, edge, lchild, rchild):
        super(EdgeNode, self).__init__(lchild, rchild)
        self.edge = edge
        
    def locate(self, edge):
        if self.edge.isAbove(edge.p): 
            return self.rchild.locate(edge)
        if self.edge.isBelow(edge.p): 
            return self.lchild.locate(edge)
        if edge.slope < self.edge.slope: 
            return self.rchild.locate(edge)
        return self.lchild.locate(edge)

class SearchGraph:
    
    def __init__(self, root):
        self.root = root
        
    def locate(self, edge):
        return self.root.locate(edge).trapezoid
  
    def followSegment(self, edge):
        trapezoids = [self.locate(edge)]
        while(trapezoids[-1] != None and edge.q.x > trapezoids[-1].rightPoint.x):
            if trapezoids[-1].rightPoint.isAbove(edge):
                trapezoids.append(trapezoids[-1].lowerRight)
            else:
                trapezoids.append(trapezoids[-1].upperRight)
        return trapezoids
  
    def replace(self, sink, node):
        if sink.parentList:
            node.replace(sink)
        else:
            self.root = node

    def trapezoidContainEdge(self, sink, edge, tlist):
        yNode = EdgeNode(edge, isSink(tlist[1]), isSink(tlist[2]))
        qNode = PointNode(edge.q, yNode, isSink(tlist[3]))
        pNode = PointNode(edge.p, isSink(tlist[0]), qNode)
        self.replace(sink, pNode)
  
    def trapezoidContainLeftEndpint(self, sink, edge, tlist):
        yNode = EdgeNode(edge, isSink(tlist[1]), isSink(tlist[2]))
        pNode = PointNode(edge.p, isSink(tlist[0]), yNode)
        self.replace(sink, pNode)
  
    def trapezoidCrossedByEdge(self, sink, edge, tlist):
        yNode = EdgeNode(edge, isSink(tlist[0]), isSink(tlist[1]))
        self.replace(sink, yNode)

    def trapezoidContainRightEndpint(self, sink, edge, tlist):
        yNode = EdgeNode(edge, isSink(tlist[0]), isSink(tlist[1]))
        qNode = PointNode(edge.q, yNode, isSink(tlist[2]))
        self.replace(sink, qNode)

def isSink(trapezoid):
    if trapezoid.sink is None: 
        return LeafNode(trapezoid)
    return trapezoid.sink
