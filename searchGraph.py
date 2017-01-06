class Node(object):

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

class Sink(Node):
        
    def __init__(self, trapezoid):
        super(Sink, self).__init__(None, None)
        self.trapezoid = trapezoid
        trapezoid.sink = self
        
    def locate(self, edge): 
        return self

class XNode(Node):

    def __init__(self, point, lchild, rchild):
        super(XNode, self).__init__(lchild, rchild)
        self.point = point
    
    def locate(self, edge): 
        if edge.p.x >= self.point.x: 
            return self.rchild.locate(edge)
        return self.lchild.locate(edge)

class YNode(Node):
    
    def __init__(self, edge, lchild, rchild):
        super(YNode, self).__init__(lchild, rchild)
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
    
    def __init__(self, head):
        self.head = head
        
    def locate(self, edge):
        return self.head.locate(edge).trapezoid
  
    def followEdge(self, edge):
        trapezoids = [self.locate(edge)]
        while(edge.q.x > trapezoids[-1].rightPoint.x):
            if edge.isAbove(trapezoids[-1].rightPoint):
                trapezoids.append(trapezoids[-1].upperRight)
            else:
                trapezoids.append(trapezoids[-1].lowerRight)
        return trapezoids
  
    def replace(self, sink, node):
        if sink.parentList:
            node.replace(sink)
        else:
            self.head = node

    def case1(self, sink, edge, tlist):
        yNode = YNode(edge, isSink(tlist[1]), isSink(tlist[2]))
        qNode = XNode(edge.q, yNode, isSink(tlist[3]))
        pNode = XNode(edge.p, isSink(tlist[0]), qNode)
        self.replace(sink, pNode)
  
    def case2(self, sink, edge, tlist):
        yNode = YNode(edge, isSink(tlist[1]), isSink(tlist[2]))
        pNode = XNode(edge.p, isSink(tlist[0]), yNode)
        self.replace(sink, pNode)
  
    def case3(self, sink, edge, tlist):
        yNode = YNode(edge, isSink(tlist[0]), isSink(tlist[1]))
        self.replace(sink, yNode)

    def case4(self, sink, edge, tlist):
        yNode = YNode(edge, isSink(tlist[0]), isSink(tlist[1]))
        qNode = XNode(edge.q, yNode, isSink(tlist[2]))
        self.replace(sink, qNode)

def isSink(trapezoid):
    if trapezoid.sink is None: 
        return Sink(trapezoid)
    return trapezoid.sink
