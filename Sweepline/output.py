import os
import matplotlib.pyplot
import sweepline
from shapes import Point, Edge, Direction
from timeit import default_timer as timer

def show(p):
    for tuple in p.edges:
        edge = tuple[0]
        matplotlib.pyplot.plot([edge.get_left_point().x, edge.get_right_point().x],[edge.get_left_point().y, edge.get_right_point().y], linestyle="-", linewidth = 2, color="k" if tuple[1] else "c")

def read(openfile):
    loc = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(loc, openfile), 'r') as f:
        content = f.readlines()
        f.closed
    return content

#Delete blanklines of infile
def delete_blanklines():
    infp = open('data.txt', "r")
    outfp = open('data_1', "w")
    lines = infp.readlines()
    for li in lines:
        if li.split():
            outfp.writelines(li)
    infp.close()
    outfp.close()

def edge_list(points):
    former_point = None
    edges = []
    for text in points:
        Line = text.split()
        if len(Line) == 1 and points[0] == text:
            None
        else:
            point = Point(int(Line[0]), int(Line[1]))
            if former_point != None:
                edges.append(Edge(former_point, point, Direction.Right))
            former_point = point
    edges.append(Edge(edges[len(edges)-1].q, edges[0].p, Direction.Right))
    return edges

def Dict(text, dist):
    min_x = 0
    i = 0
    for text in text:
        l = text.split()
        if (len(l) == 1) and (text[0] == text):
            min_x = int(l[0])
        elif len(l) > 1:
            if i < min_x:
                dist[i] = [l[0], l[1]]
                i += 1
    if (i < min_x):
        print("Need points!")
        dist.clear()

# Empty output file
f = open('output', 'w')
f.truncate()
#Begin to record the running time
timing=0.0
start_time = timer()
delete_blanklines()
# According to the value of data to adjust the final result visualization here
adjust =1
# Construct edges list
edges = edge_list(read('data_1'))
# Calculate limits
# put coordinates of any point here
# Initinalize
line = edges[0]
minx = line.p.x
maxx = line.p.x
miny = line.p.y
maxy = line.p.y
for line in edges:
    minx = min(minx, line.p.x, line.q.x)
    maxx = max(maxx, line.p.x, line.q.x)
    miny = min(miny, line.p.y, line.q.y)
    maxy = max(maxy, line.p.y, line.q.y)

# Create bounding box
minx = minx-adjust
maxx = maxx+adjust
miny = miny-adjust
maxy = maxy+adjust

# Construct trapezoidal map
td = sweepline.trapezoid_decompose(edges)
# End timing
end_time = timer()
timing=start_time-end_time
if timing:
    print('Running time: {0:.4f}'.format(end_time - start_time))

#Visualization of results
matplotlib.pyplot.axes()
matplotlib.pyplot.ylim([miny, maxy])
matplotlib.pyplot.xlim([minx, maxx])
show(td)
matplotlib.pyplot.show()