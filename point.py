class Point(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next, self.prev = None, None

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y) 
        else:
            return Point(self.x - other, self.y - other)
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y) 
        else:
            return Point(self.x + other, self.y + other)