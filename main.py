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

# from polygonGenerator.generate import generatePolygon

# star = generatePolygon(250, 250, 200, .8, .8, 2)
Epsilon = 1e-5

def connectPoints(points):
    edgeList = []
    numberOfPoints = len(points)
    for idx, point in enumerate(points):
        next = idx + 1 if idx < numberOfPoints-1 else 0
        p = points[idx][0], points[idx][1]
        q = points[next][0], points[next][1]

        # if p[0] == q[0]:
        #     sys.exit('Detect vertical edge!')

        edgeList.append((p, q))

    return randomizeEdgeOrder(edgeList)

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

def randomizeEdgeOrder(edgeList):
    edges = []
    for e in edgeList:
        p = shearTransformation(e[0])
        q = shearTransformation(e[1])

        if p.x > q.x:
            edges.append(Edge(q, p))
        else:
            edges.append(Edge(p, q))
    
    seed()
    shuffle(edges)
    return edges

def shearTransformation(point):
    return Point(point[0] + Epsilon * point[1], point[1])

def main():
    
    star = [(73, 224), (65, 183), (36, 120), (110, 120), (127, 74), (171, 62), (215, 72), (253, 37), (295, 56), (334, 71), (373, 90), (419, 105), (433, 149), (411, 200), (427, 234), (457, 276), (464, 325), (419, 356), (372, 367), (353, 405), (320, 424), (283, 443), (241, 475), (203, 434), (178, 400), (132, 402), (69, 401), (67, 346), (85, 298), (38, 265)] 
    trapezoidize = Trapezoidize(connectPoints(star), makeBoundingBox())

    trapezoids = trapezoidize.trapezoids

    plt.figure()
    for t in trapezoids:

        vertices = t.vertices()
        plt.gca().add_patch(PolygonPatch(Polygon(vertices)))
        plt.gca().autoscale(tight=True)

    plt.show()

if __name__ == '__main__':
    main()