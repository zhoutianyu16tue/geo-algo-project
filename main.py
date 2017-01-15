# -*- coding: utf-8 -*-
from trapezoidize import Trapezoidize
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import  Polygon
from point import Point
from edge import Edge
from random import shuffle, seed
import sys
from trapezoid import Trapezoid
import numpy as np
import math

# from polygonGenerator.generate import generatePolygon

# star = generatePolygon(250, 250, 200, .8, .8, 2)
Epsilon = 1e-6

def makeRandomOrderEdges(points):
    edges = []
    numberOfPoints = len(points)

    for idx, point in enumerate(points):
        next = idx + 1 if idx < numberOfPoints-1 else 0

        # Shear transformation
        p = Point(points[idx][0] + Epsilon * points[idx][1], points[idx][1])
        q = Point(points[next][0] + Epsilon * points[next][1], points[next][1])
        edges.append(Edge(p, q))
    
    seed()
    shuffle(edges)
    return edges

def makeBoundingBox():
    # use the infinite box as the bounding box
    maxX = sys.maxsize
    maxY = maxX
    minX = -sys.maxsize + 1
    minY = minX
    top = Edge(Point(minX, maxY), Point(maxX, maxY))
    bottom = Edge(Point(minX, minY), Point(maxX, minY))
    left = Point(minX, maxY)
    right = Point(maxX, maxY)

    return Trapezoid(left, right, top, bottom)

def readData(fileName):
    points = []
    with open(fileName, 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            tmp = line.split()
            points.append((int(tmp[0]),int(tmp[1])))

    return points

numOfTestPerSet = 20
numOfSet = 2100
showRunningTime = []
listOfTestSet = list(range(100, numOfSet, 100))

def main():
    
    # runningTimes = []
    # for num in listOfTestSet:
    #     curNumRunningTimeList = []
    #     fileName = './testData/%d.txt' % num
    #     star = readData(fileName)
    #     for i in range(numOfTestPerSet):
    #         print('Runing %d dataSet for %d time.' % (num, i+1))
    #         trapezoidize = Trapezoidize(makeRandomOrderEdges(star), makeBoundingBox())
    #         curNumRunningTimeList.append(trapezoidize.runningTime)
    #     # print(curNumRunningTimeList)
    #     runningTimes.append(curNumRunningTimeList)

    # for idx, runningTime in enumerate(runningTimes):
    #     runningTime.sort()
    #     print((idx+1)*100, sum(runningTime[2:-2]) / (numOfTestPerSet - 4))
    #     showRunningTime.append(sum(runningTime[2:-2]) / (numOfTestPerSet - 4))

    # plt.scatter(listOfTestSet, showRunningTime)
    # plt.show()
    # trapezoids = trapezoidize.trapezoids

    # plt.figure()
    # star = readData(sys.argv[1])
    # trapezoidize = Trapezoidize(makeRandomOrderEdges(star), makeBoundingBox())

    # print('It takes %f ms' % trapezoidize.runningTime)
    # for t in trapezoidize.trapezoids:
    #     vertices = t.vertices()
    #     plt.gca().add_patch(PolygonPatch(Polygon(vertices)))
    #     plt.gca().autoscale(tight=True)

    # plt.show()

if __name__ == '__main__':
    main()