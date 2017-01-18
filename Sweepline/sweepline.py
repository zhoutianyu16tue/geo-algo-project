from enum import IntEnum
from bintrees import avltree
from shapes import Edge,Status, Direction, Decomposition,Event,EventType,Sta

def build_event_queue(edges):#only insert left point of each edge here
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
    #use a tree here to do operation on event queue easier(can only use list)
    for evt in events:
        if evt.index == index:
            evts.append(evt)
        else:
            if len(evts) > 0:
                tree.insert(index, evts)
            evts = []
            index = evt.index
            evts.append(evt)
    tree.insert(index, evts)
    return tree

def build_potential_status(edges):
    statu = []
    for edge in edges:
        statu.append(Sta(edge.get_left_point().y,edge))
    return statu

def add_edges(status, targetX, E,event_edge, trapezoid_decomposition):
    upper = None
    lower = None
    for key in E:
        edge = E[key]
        status.insert(edge.statusForEdge(), edge)
    key = event_edge.statusForEdge()
    try:#find two edges most close the edge(where event point locates)
        upper = status.prev_item(key)#reture succ item to key
    except KeyError:
        None
    try:
        lower = status.succ_item(key)#return prev item to key

    except KeyError:
        None
    f = open('output', 'a')
    if upper != None and (upper[1].is_left_to_right() and upper[1].WhichSide == Direction.Right):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(upper[1].point_at_edge(targetX).x, upper[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        trapezoid_decomposition.add_vertex_edge(Edge(event_edge.point_at_edge(targetX), upper[1].point_at_edge(targetX), Direction.Both))
    if upper != None and  (upper[1].is_right_to_left() and upper[1].WhichSide == Direction.Left):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(upper[1].point_at_edge(targetX).x, upper[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        trapezoid_decomposition.add_vertex_edge(
            Edge(event_edge.point_at_edge(targetX), upper[1].point_at_edge(targetX), Direction.Both))
    if lower != None and (lower[1].is_right_to_left() and lower[1].WhichSide == Direction.Right):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(lower[1].point_at_edge(targetX).x, lower[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        trapezoid_decomposition.add_vertex_edge(Edge(event_edge.point_at_edge(targetX), lower[1].point_at_edge(targetX), Direction.Both))
    if lower != None and (lower[1].is_left_to_right() and lower[1].WhichSide == Direction.Left):
        #i = "({}, {}),".format(edge.point_at_edge(targetX).x, edge.point_at_edge(targetX).y)
        #j = "({}, {})".format(lower[1].point_at_edge(targetX).x, lower[1].point_at_edge(targetX).y)
        #print('Added Edge :' + str(i + j))
        trapezoid_decomposition.add_vertex_edge(Edge(event_edge.point_at_edge(targetX), lower[1].point_at_edge(targetX), Direction.Both))
    return


def getKey(Sta):
    return Sta.y_coordinate

def trapezoid_decompose(edges):
    # Construct event queue firstly
    event_queue = build_event_queue(edges)
    # Initialize status
    status = avltree.AVLTree()
    # Handle events
    trapezoid_decomposition = Decomposition()
    while len(event_queue) > 1:
        min_=event_queue.min_item()
        event_edge=min_[1][0].edge
        remove_y=min_[1][0].edge.get_left_point().y # the y-coordinate of this event point
        event_T = event_queue.pop_min()
        for evt in event_T[1]:
            points = {};
            targetX = evt.index
            if evt.type == EventType.Insert:
                status.insert(evt.edge.statusForEdge(), evt.edge)
                trapezoid_decomposition.add_edge(evt.edge)
            if evt.type == EventType.Removal:
                status.remove(evt.edge.statusForEdge())
        #find the edges intersecting with sweep edge
        event_A=build_potential_status(edges)
        event_A.pop(remove_y)
        event_A=sorted(event_A, key=getKey) # sort the edges according to y-coordinate
        for e in event_A:
            realY = e.edge.point_at_edge(targetX).y # y-coordinate potential of intersection point
            #check whether these edges are intersected with sweep line, add these points indeed intersect with event point
            if (((realY>=e.edge.get_left_point().y) and (realY<=e.edge.get_right_point().y))
                or ((realY>=e.edge.get_right_point().y)and(realY<=e.edge.get_left_point().y)))and ((targetX<=e.edge.get_right_point().x)and(targetX>=e.edge.get_left_point().x)):
                points[realY]= e.edge
                #points are the edges, which really have intersection points with sweep line
        add_edges(status, targetX, points, event_edge,trapezoid_decomposition)
    return trapezoid_decomposition
