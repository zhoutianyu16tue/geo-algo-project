# -*- coding: utf-8 -*-
from trapezoidize import Trapezoidize
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import  Polygon
# from polygonGenerator.generate import generatePolygon

# star = generatePolygon(250, 250, 200, .8, .8, 2)
star = [(341, 131), (361, 170), (506, 174), (544, 262), (446, 321), (418, 383), (354, 404), (291, 382), (245, 496), (176, 465), (148, 384), (121, 342), (133, 291), (24, 257), (57, 191), (106, 145), (132, 87), (207, 118), (252, 92), (316, 70)]
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