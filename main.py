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

def makeRandomOrderEdges(points):
    edges = []
    numberOfPoints = len(points)

    for idx, point in enumerate(points):
        next = idx + 1 if idx < numberOfPoints-1 else 0

        # Shear transformation
        p = Point(points[idx][0] + Epsilon * points[idx][1], points[idx][1])
        q = Point(points[next][0] + Epsilon * points[next][1], points[next][1])

        if p.x > q.x:
            edges.append(Edge(q, p))
        else:
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

def main():
    
    star = [(-55, 460), (-211, 250), (-43, 29), (125, -206), (376, -126), (620, 12), (648, 250), (558, 476), (363, 654), (149, 570)]
    trapezoidize = Trapezoidize(makeRandomOrderEdges(star), makeBoundingBox())

    trapezoids = trapezoidize.trapezoids

    plt.figure()
    for t in trapezoids:

        vertices = t.vertices()
        plt.gca().add_patch(PolygonPatch(Polygon(vertices)))
        plt.gca().autoscale(tight=True)

    plt.show()

if __name__ == '__main__':
    main()