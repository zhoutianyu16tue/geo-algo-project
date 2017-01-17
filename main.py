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
from trapezoidize import N

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

numOfTestPerSet = 10
numOfSet = 55000
showRunningTime = []
listOfTestSet = list(range(10000, numOfSet, 5000))

def main():
    
    # runningTimes = []
    # for num in listOfTestSet:
    #     curNumRunningTimeList = []
    #     fileName = './50000Star/Star%d.txt' % num
    #     star = readData(fileName)
    #     for i in range(numOfTestPerSet):
    #         print('Runing %d dataSet for %d time.' % (num, i+1))
    #         trapezoidize = Trapezoidize(makeRandomOrderEdges(star), makeBoundingBox())
    #         curNumRunningTimeList.append(trapezoidize.runningTime)
    #         del trapezoidize.trapezoidalMap
    #         del trapezoidize.searchGraph
    #         del trapezoidize.trapezoids
    #         del trapezoidize.edges
    #         del trapezoidize
    #     # print(curNumRunningTimeList)
    #     runningTimes.append(curNumRunningTimeList)

    # for idx, runningTime in enumerate(runningTimes):
    #     runningTime.sort()
    #     print((idx+1)*100, sum(runningTime[2:-2]) / (numOfTestPerSet - 4))
    #     showRunningTime.append(sum(runningTime[2:-2]) / (numOfTestPerSet - 4))

    # plt.scatter(listOfTestSet, showRunningTime)
    # plt.show()

    # runningTimes = []
    # fileName = sys.argv[1]
    # star = readData(fileName)
    # for i in range(numOfTestPerSet):
    #     print('Runing %s dataSet for %d time.' % (fileName, i+1))
    #     trapezoidize = Trapezoidize(makeRandomOrderEdges(star), makeBoundingBox())
    #     runningTimes.append(trapezoidize.runningTime)
    #     del trapezoidize
    # # print(curNumRunningTimeList)

    # runningTimes.sort()
    # print(runningTimes)
    # print('running time: %f' % (sum(runningTimes[2:-2]) / (numOfTestPerSet - 4)))


    plt.figure()
    # star = readData(sys.argv[1])
    # plt.gca().add_patch(PolygonPatch(Polygon(star)))
    # plt.gca().autoscale(tight=True)
    # plt.show()
    star = [(434, 148), (416, 223), (476, 279), (450, 340), (404, 396), (322, 390), (277, 432), (219, 446), (183, 389), (108, 398), (75, 343), (41, 286), (38, 218), (63, 163), (121, 123), (167, 93), (220, 89), (274, 78), (325, 84), (379, 102)]
    trapezoidize = Trapezoidize(makeRandomOrderEdges(star), makeBoundingBox())
    print('It takes %f ms' % trapezoidize.runningTime)
    print('trapezoidize.startingFromRoot: %d' % trapezoidize.startingFromRoot)
    print('N(h-1) ~ N(h): %d' % N(len(star), 1))
    for t in trapezoidize.trapezoids:
        vertices = t.vertices()
    # vertices = star
        plt.gca().add_patch(PolygonPatch(Polygon(vertices)))
        plt.gca().autoscale(tight=True)

    plt.show()

if __name__ == '__main__':
    main()