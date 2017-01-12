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
    star = [(-55, 523), (-191, 107), (37, -107), (291, -89), (578, -112), (610, 155), (604, 453), (290, 591)]
    star = [(562, 452), (703, 585), (418, 402), (611, 627), (520, 576), (494, 587), (492, 649), (345, 445), (442, 726), (406, 770), (318, 591), (311, 690), (264, 504), (249, 616), (216, 646), (192, 562), (191, 469), (139, 559), (160, 456), (70, 574), (-30, 659), (41, 512), (-68, 598), (147, 349), (-157, 581), (-69, 462), (-71, 421), (-93, 391), (2, 324), (-60, 309), (-176, 299), (-428, 274), (-35, 236), (-243, 192), (-258, 159), (-126, 144), (-238, 60), (-15, 120), (-67, 71), (-148, -11), (16, 64), (-188, -159), (-45, -59), (49, 12), (168, 136), (6, -150), (48, -151), (16, -323), (129, -161), (150, -180), (156, -363), (233, -9), (253, -32), (284, -61), (360, -307), (398, -250), (402, -146), (331, 68), (437, -85), (539, -203), (520, -114), (465, 8), (452, 58), (465, 69), (524, 57), (424, 147), (681, 45), (503, 156), (829, 76), (787, 127), (676, 180), (703, 204), (811, 248), (860, 303), (843, 334), (771, 373), (691, 381), (674, 413), (639, 425), (701, 487)]
    star = [(257, -79), (320, -30), (448, -195), (397, 21), (489, 17), (702, -69), (884, -7), (534, 211), (590, 277), (463, 307), (544, 381), (401, 364), (376, 401), (405, 563), (306, 530), (224, 727), (196, 429), (132, 499), (18, 563), (-111, 557), (-72, 443), (-18, 351), (-37, 279), (-359, 192), (-272, 105), (40, 144), (-132, -51), (164, 132), (43, -234), (125, -331)]
    star = [(26, 175), (-174, -21), (-36, -4), (-6, -63), (47, -126), (159, -118), (258, -109), (301, -29), (431, -170), (538, -111), (478, 49), (491, 129), (613, 169), (711, 240), (781, 384), (490, 350), (672, 559), (422, 446), (492, 691), (364, 579), (297, 626), (222, 562), (138, 666), (183, 389), (91, 467), (-120, 555), (38, 375), (-46, 349), (-91, 276), (-171, 194)]
    star = [(591, 50), (692, 110), (691, 214), (577, 290), (597, 364), (538, 413), (499, 477), (440, 506), (413, 619), (329, 631), (255, 610), (166, 665), (93, 626), (2, 596), (-36, 512), (-56, 427), (-161, 389), (-111, 288), (-157, 201), (-139, 111), (-111, 18), (-70, -57), (3, -116), (82, -146), (173, -160), (260, -94), (341, -131), (409, -82), (506, -91), (565, -26)]
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