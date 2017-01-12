class Node():

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.parentList = []
        if left != None: 
            left.parentList.append(self)
        if right != None: 
            right.parentList.append(self)
        
    def insert(self, node):
        for parent in node.parentList:
            if parent.left is node: 
                parent.left = self
            else: 
                parent.right = self 
        self.parentList += node.parentList

class LeafNode(Node):
        
    def __init__(self, trapezoid):
        super(LeafNode, self).__init__(None, None)
        self.trapezoid = trapezoid
        
    def find(self, edge): 
        return self

class PointNode(Node):

    def __init__(self, point, left, right):
        super(PointNode, self).__init__(left, right)
        self.point = point
    
    def find(self, edge): 
        if edge.p.x >= self.point.x: 
            return self.right.find(edge)
        return self.left.find(edge)

class EdgeNode(Node):
    
    def __init__(self, edge, left, right):
        super(EdgeNode, self).__init__(left, right)
        self.edge = edge
        
    def find(self, edge):
        if self.edge.isAbove(edge.p): 
            return self.right.find(edge)
        if self.edge.isBelow(edge.p): 
            return self.left.find(edge)
        if edge.slope < self.edge.slope: 
            return self.right.find(edge)
        return self.left.find(edge)

class SearchGraph:
    
    def __init__(self, root):
        self.root = root
        
    def find(self, edge):
        return self.root.find(edge).trapezoid
  
    def followSegment(self, edge):
        trapezoids = [self.find(edge)]
        while(trapezoids[-1] != None and edge.q.x > trapezoids[-1].rightPoint.x):
            if trapezoids[-1].rightPoint.isAbove(edge):
                trapezoids.append(trapezoids[-1].lowerRight)
            else:
                trapezoids.append(trapezoids[-1].upperRight)

        return trapezoids
  
    def insert(self, leaf, newNode):
        if len(leaf.parentList) > 0:
            # the leaf is not the root
            newNode.insert(leaf)
        else:
            self.root = newNode

    def trapezoidContainEdge(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[1].node, newTrapezoids[2].node)
        qNode = PointNode(edge.q, yNode, newTrapezoids[3].node)
        pNode = PointNode(edge.p, newTrapezoids[0].node, qNode)

        self.insert(leaf, pNode)
  
    def trapezoidContainLeftEndpint(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[1].node, newTrapezoids[2].node)
        pNode = PointNode(edge.p, newTrapezoids[0].node, yNode)

        self.insert(leaf, pNode)
  
    def trapezoidCrossedByEdge(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[0].node, newTrapezoids[1].node)

        self.insert(leaf, yNode)

    def trapezoidContainRightEndpint(self, leaf, edge, newTrapezoids):
        yNode = EdgeNode(edge, newTrapezoids[0].node, newTrapezoids[1].node)
        qNode = PointNode(edge.q, yNode, newTrapezoids[2].node)
        
        self.insert(leaf, qNode)