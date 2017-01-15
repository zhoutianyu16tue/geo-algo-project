import os
import matplotlib.pyplot
import sweepline
from shapes import Point, Edge, Direction
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from random import shuffle, seed
from datetime import datetime

Epsilon = 1e-6
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
def delete_blanklines(fileName):
    infp = open(fileName, "r")
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
                former_point=Point(former_point.x + Epsilon * former_point.y , former_point.y)
                point = Point(point.x + Epsilon * point.y , point.y)
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


numOfTestPerSet = 20
#numOfSet = 2100
numOfSet = 2100
showRunningTime = []
listOfTestSet = list(range(100, numOfSet, 100))
runningTimes = []
for num in listOfTestSet:
    # Empty output file
    f = open('output', 'w')
    f.truncate()
    curNumRunningTimeList = []
    #fileName = './PolygonData/%d.txt' % num
    fileName = './PolygonData/%d.txt' % num
    infp = open(fileName, "r")
    outfp = open('data_1', "w")
    lines = infp.readlines()
    for li in lines:
        if li.split():
            outfp.writelines(li)
    infp.close()
    outfp.close()
    for i in range(numOfTestPerSet):
        print('Runing %d dataSet for %d time.' % (num, i+1))
        edges = edge_list(read('data_1'))
        timing = 0.0
        start_time = datetime.now()
        # delete_blanklines(fileName)
        td = sweepline.trapezoid_decompose(edges)
        end_time = datetime.now()
        timing = end_time - start_time
        curNumRunningTimeList.append((timing.total_seconds()*1000))
        #print(timing)
    runningTimes.append(curNumRunningTimeList)
for idx, runningTime in enumerate(runningTimes):
    runningTime.sort()
    print((idx + 1) * 100, sum(runningTime[2:-2]) / (numOfTestPerSet - 4))
    showRunningTime.append(sum(runningTime[2:-2]) / (numOfTestPerSet - 4))
plt.scatter(listOfTestSet, showRunningTime)
plt.show()