from enum import IntEnum
from bintrees import avltree
from shapes import Edge,Status, Direction, Decomposition
class Event:
    def __init__(self, edge, type, index):
        self.edge = edge
        self.type = type
        self.index = index

class EventType(IntEnum):
    Insert = 1
    Removal = 2
    Nothing = 3

def build_event_queue(edges):
    tree = avltree.AVLTree() # avltree is a subclass of BinarySearchTree
    events = []
    for edge in edges:
        if edge.p.x < edge.q.x or (edge.p.x == edge.q.x and edge.p.y < edge.q.y):
            events.append(Event(edge, EventType.Insert, edge.p.x))
            events.append(Event(edge, EventType.Removal, edge.q.x))
        else:
            events.append(Event(edge, EventType.Removal, edge.p.x))
            events.append(Event(edge, EventType.Insert, edge.q.x))
    events = sorted(events, key=lambda evt: (evt.index, evt.type))
    index = -1
    evts = []

    for evt in events:
        if evt.index == index:
            evts.append(evt)
        else:
            if len(evts) > 0:
                if type == EventType.Insert:
                    tree.insert(index, evts)
                else:
                    tree.insert(index, evts)

            evts = []
            index = evt.index
            evts.append(evt)
    tree.insert(index, evts)
    return tree

def add_edges(status, targetX, edge, trapezoid_decomposition):
    upper = None
    lower = None
    key = Status(edge.point_at_edge(targetX).y, 0)
    try:#find two edges most close the edge(where event point locates)
        upper = status.ceiling_item(key)#reture(k,v) k is the smallest key greater than or equal to key
    except KeyError:
        None
    try:
        lower = status.floor_item(key)#get (k, v) pair, where k is the greatest key less than or equal to key
    except KeyError:
        None
    f = open('output', 'a')
    if upper != None and (upper[1].is_left_to_right() and upper[1].WhichSide == Direction.Right):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(upper[1].point_at_edge(targetX).x, upper[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        #f.write(str(i + j) + '\n')
        trapezoid_decomposition.add_vertex_edge(Edge(edge.point_at_edge(targetX), upper[1].point_at_edge(targetX), Direction.Both))
    if upper != None and  (upper[1].is_right_to_left() and upper[1].WhichSide == Direction.Left):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(upper[1].point_at_edge(targetX).x, upper[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        #f.write(str(i + j) + '\n')
        trapezoid_decomposition.add_vertex_edge(
            Edge(edge.point_at_edge(targetX), upper[1].point_at_edge(targetX), Direction.Both))
    if lower != None and (lower[1].is_right_to_left() and lower[1].WhichSide == Direction.Right):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(lower[1].point_at_edge(targetX).x, lower[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        #f.write(str(i + j) + '\n')
        trapezoid_decomposition.add_vertex_edge(Edge(edge.point_at_edge(targetX), lower[1].point_at_edge(targetX), Direction.Both))
    if lower != None and (lower[1].is_left_to_right() and lower[1].WhichSide == Direction.Left):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(lower[1].point_at_edge(targetX).x, lower[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        #f.write(str(i + j) + '\n')
        trapezoid_decomposition.add_vertex_edge(Edge(edge.point_at_edge(targetX), lower[1].point_at_edge(targetX), Direction.Both))
    return



def trapezoid_decompose(edges):
    # Construct event queue firstly
    event_queue = build_event_queue(edges)
    # Initialize status
    status = avltree.AVLTree()
    # Handle events
    trapezoid_decomposition = Decomposition()
    while len(event_queue) > 1:
        event_T = event_queue.pop_min()
        draw_td_edge = False
        for evt in event_T[1]:
            targetX = evt.index
            if not draw_td_edge and (evt.type == EventType.Insert):
                add_edges(status, targetX, evt.edge, trapezoid_decomposition)
                draw_td_edge = True
            if evt.type == EventType.Insert:
                status.insert(evt.edge.statusForEdge(), evt.edge)
                trapezoid_decomposition.add_edge(evt.edge)
            if evt.type == EventType.Removal:
                status.remove(evt.edge.statusForEdge())
        if not draw_td_edge:
            add_edges(status, targetX, event_T[1][0].edge, trapezoid_decomposition)
            draw_td_edge = True
    return trapezoid_decomposition
