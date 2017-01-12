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
  
    def replace(self, leaf, node):
        if leaf.parentList:
            node.replace(leaf)
        else:
            self.root = node

    def trapezoidContainEdge(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[1].node, newTrapezoids[2].node)
        qNode = PointNode(edge.q, yNode, newTrapezoids[3].node)
        pNode = PointNode(edge.p, newTrapezoids[0].node, qNode)
        self.replace(leaf, pNode)
  
    def trapezoidContainLeftEndpint(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[1].node, newTrapezoids[2].node)
        pNode = PointNode(edge.p, newTrapezoids[0].node, yNode)
        self.replace(leaf, pNode)
  
    def trapezoidCrossedByEdge(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[0].node, newTrapezoids[1].node)
        self.replace(leaf, yNode)

    def trapezoidContainRightEndpint(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[0].node, newTrapezoids[1].node)
        qNode = PointNode(edge.q, yNode, newTrapezoids[2].node)
        self.replace(leaf, qNode)