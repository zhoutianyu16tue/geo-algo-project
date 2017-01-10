from enum import Enum
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def point_lies_on_edge(self, edge):
        # Use Cross Product of vectors to decide whether point is on the edge
        if edge.isLeftToRight():
            left_point = edge.p
            right_point = edge.q
        else:
            left_point = edge.q
            right_point = edge.p

        vector_1 = Point(right_point.x-left_point.x, right_point.y-left_point.y)
        vector_2 = Point(self.x-left_point.x, self.y-left_point.y)
        cross_product = vector_1.x * vector_2.y - vector_1.y * vector_2.x
        return cross_product < 0

# Edge (p to q)
class Edge:
    def __init__(self, p, q, WhichSide):
        self.p = p
        self.q = q
        self.WhichSide = WhichSide # WhichSide shows which side of the edges(left, right , or both ) is in the polygon

    def __repr__(self):
        return "({}, {})".format(self.p, self.q)

    def left_point_y(self):
        if self.p.x<self.q.x :
            return self.p.y
        else:
            return self.q.y

    def get_left_point(self):
        if self.p.x < self.q.x:
            return self.p
        else:
            return self.q

    def get_right_point(self):
        if self.p.x < self.q.x:
            return self.q
        else:
            return self.p

    def edge_slope(self):
        dx = self.get_right_point().x - self.get_left_point().x
        dy = self.get_right_point().y - self.get_left_point().y
        return dy/dx
    def statusKeyForEdge(self):
        dx = self.get_right_point().x - self.get_left_point().x
        dy = self.get_right_point().y - self.get_left_point().y
        return StatusKey(self.get_left_point().y, dy / dx)

    def point_at_edge(self, targetX):
        return Point(targetX, self.get_left_point().y + (targetX - self.get_left_point().x) * self.edge_slope())

    def is_left_to_right(self):
        return self.p.x < self.q.x

    def is_right_to_left(self):
        return self.p.x > self.q.x


class StatusKey:
    def __init__(self, left_point_y, dxdy):
        self.left_point_y = left_point_y
        self.dxdy = dxdy

    def __repr__(self):
        return "(start: {}, dxdy: {})".format(self.left_point_y, self.dxdy)


class Direction(Enum):
    Left = 1
    Right = 2
    Both = 3

class VerticalDecomposition:
    # list of tuples (a, b) where a is an edge in the decomposition and b is true iff a is an edge of the original
    # polygon.
    edges = []
    def addEdge(self, edge):
        self.edges.append((edge, True))
    def addVertEdge(self, edge):
        self.edges.append((edge, False))
