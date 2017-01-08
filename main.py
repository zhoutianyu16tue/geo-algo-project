# -*- coding: utf-8 -*-
from trapezoidize import Trapezoidize
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import  Polygon
# from polygonGenerator.generate import generatePolygon

# star = generatePolygon(250, 250, 200, .8, .8, 2)
star = [(285, 194), (419, 100), (413, 156), (360, 217), (513, 242), (407, 281), (521, 387), (505, 483), (437, 457), (348, 429), (252, 260), (254, 455), (241, 393), (219, 342), (160, 427), (96, 434), (224, 276), (0, 411), (-14, 375), (-26, 348), (-7, 260), (45, 219), (17, 175), (76, 135), (46, 10), (163, 88), (169, 25), (248, 218), (313, -78), (305, 66)]
star.reverse()
trapezoidize = Trapezoidize(star)

trapezoids = trapezoidize.trapezoids

plt.figure()
for t in trapezoids:

    vertices = t.vertices()
    plt.gca().add_patch(PolygonPatch(Polygon(vertices)))
    plt.gca().autoscale(tight=True)

plt.show()