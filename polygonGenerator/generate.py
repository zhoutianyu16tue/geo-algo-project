import math, random
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import  Polygon
import sys

def generatePolygon( ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts ) :
# '''Start with the centre of the polygon at ctrX, ctrY, 
#     then creates the polygon by sampling points on a circle around the centre. 
#     Randon noise is added by varying the angular spacing between sequential points,
#     and by varying the radial distance of each point from the centre.

#     Params:
#     ctrX, ctrY - coordinates of the "centre" of the polygon
#     aveRadius - in px, the average radius of this polygon, this roughly controls how large the polygon is, really only useful for order of magnitude.
#     irregularity - [0,1] indicating how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]
#     spikeyness - [0,1] indicating how much variance there is in each vertex from the circle of radius aveRadius. [0,1] will map to [0, aveRadius]
#     numVerts - self-explanatory

#     Returns a list of vertices, in CCW order.
# '''

    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts) :
        tmp = random.uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2*math.pi)
    for i in range(numVerts) :
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts) :
        r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( (int(x),int(y)) )

        angle = angle + angleSteps[i]

    return points

def clip(x, min, max) :
    if( min > max ) :  return x    
    elif( x < min ) :  return min
    elif( x > max ) :  return max
    else :             return x

print('usage: python3 generate.py averageRadius irregularity spikeyness numVerts')

verts = generatePolygon(ctrX=250, ctrY=250, aveRadius=int(sys.argv[1]), irregularity=float(sys.argv[2]), spikeyness=float(sys.argv[3]), numVerts=int(sys.argv[4]))
print(verts)
# for num in range(100,1500,50):
#     vertices = generatePolygon(250, 250, 200, .1, .2, num)
#     with open('../testData/Star%d.txt' % num, 'w+') as fd:
#         for vertex in vertices:
#             fd.write('%d %d\n' % (vertex[0], vertex[1]))
#         print('Write %d vertices.' % num)
# print('Done!')
# plt.figure()

plt.gca().add_patch(PolygonPatch(Polygon(verts)))
plt.gca().autoscale(tight=True)
plt.show()

