from enum import Enum

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

# Edge (p to q)
class Edge:
    def __init__(self, p, q, WhichSide):
        self.p = p
        self.q = q
        self.WhichSide = WhichSide # WhichSide shows which side of the edges(left, right , or both ) is in the polygon

    def __repr__(self):
        return "({}, {})".format(self.p, self.q)

    def edge_slope(self):
        dx = self.get_right_point().x - self.get_left_point().x
        dy = self.get_right_point().y - self.get_left_point().y
        return dy/dx

    def statusForEdge(self):
        dx = self.get_right_point().x - self.get_left_point().x
        dy = self.get_right_point().y - self.get_left_point().y
        return Status(self.get_left_point().y, dy / dx)

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

    def point_at_edge(self, targetX):
        return Point(targetX, self.get_left_point().y + (targetX - self.get_left_point().x) * self.edge_slope())

    def is_left_to_right(self):
        return self.p.x < self.q.x

    def is_right_to_left(self):
        return self.p.x > self.q.x



# Used for the sweep line
class Status:
    def __init__(self, startAtY, dxdy):
        self.startAtY = startAtY
        self.dxdy = dxdy

    def __lt__(self, other):
        if self.startAtY == other.startAtY:
            return self.dxdy < other.dxdy
        else:
            return self.startAtY < other.startAtY

    def __eq__(self, other):
        return self.startAtY == other.startAtY and self.dxdy == other.dxdy


class Direction(Enum):
    Left = 1
    Right = 2
    Both = 3

class Decomposition:
    edges = []
    def add_edge(self, edge):
        self.edges.append((edge, True))

    def add_vertex_edge(self, edge):
        self.edges.append((edge, False))