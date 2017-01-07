# -*- coding: utf-8 -*-
from trapezoidize import Trapezoidize
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import  Polygon
# from polygonGenerator.generate import generatePolygon

# star = generatePolygon(250, 250, 200, .8, .8, 2)
star = [(365, 178), (387, 228), (429, 287), (522, 398), (528, 472), (362, 367), (452, 558), (285, 532), (210, 472), (131, 443), (250, 250), (250, 250), (-71, 288), (62, 202), (-105, 65), (218, 212), (115, -39), (227, 136), (306, -38), (307, 171)] 
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