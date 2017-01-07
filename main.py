# -*- coding: utf-8 -*-
from trapezoidize import Trapezoidize
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import  Polygon
# from polygonGenerator.generate import generatePolygon

# star = generatePolygon(250, 250, 200, .8, .8, 2)
star = [(398, 206), (369, 231), (450, 245), (471, 275), (364, 278), (372, 298), (312, 283), (298, 284), (474, 455), (406, 430), (362, 414), (306, 357), (294, 374), (278, 370), (268, 438), (241, 491), (216, 450), (188, 461), (205, 352), (202, 331), (193, 322), (61, 433), (164, 314), (111, 328), (-38, 370), (9, 318), (-41, 294), (-43, 258), (46, 229), (68, 208), (112, 199), (143, 193), (56, 114), (94, 108), (156, 142), (152, 103), (161, 74), (158, -5), (211, 81), (236, 100), (259, -13), (281, 64), (307, 56), (396, -75), (328, 118), (386, 73), (336, 162), (323, 192), (423, 143), (482, 147)] 
trapezoidize = Trapezoidize(star)

trapezoids = trapezoidize.trapezoids
#trapezoids = seidel.trapezoidal_map.

plt.figure()
for t in trapezoids:
    #t = self.trapezoids[0]
    #verts = self.trapezoids[t].vertices()
    verts = t.vertices()
    
    plt.gca().add_patch(PolygonPatch(Polygon(verts)))
    plt.gca().autoscale(tight=True)
    # print(verts)
#    plt.show()
#    for vert in verts:
#        plt.plot(vert[0], vert[1], '-')

plt.show()