import matplotlib.pyplot as plt
from pandas import DataFrame
from math import log2
import numpy as np
from scipy.optimize import curve_fit

df = DataFrame()
numOfSet = 2100
df['x'] = range(100, numOfSet, 100)
files = ['sweep', 'seidel', 'fast']
data = [[],[],[]]

def func(x, a, c, d):
    return a * x * np.log2(x + c) + d

for idx, file in enumerate(files):
    with open(file + '2000.txt', 'r') as fd:
        lines = fd.readlines()

    for line in lines:
        data[idx].append(float(line))


df['sweep'] = data[0]
df['seidel'] = data[1]
df['fast'] = data[2]

ax = df.plot(kind='scatter', x='x', y='seidel',color='Red', marker=(5, 0), s=40, label='seidel');
df.plot(kind='scatter', x='x', y='sweep',color='Blue', ax=ax, marker=(5, 1), s=40, label='sweep');
df.plot(kind='scatter', x='x', y='fast',color='Green', ax=ax, marker=(5, 3), s=40, label='fast');
plt.xlabel('number of points of the polygon')
plt.ylabel('running time(ms)')
plt.title('Title here')
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=numOfSet)
plt.legend(loc='upper left')

parameter, covariance_matrix = curve_fit(func, df['x'], df['sweep'])
plt.plot(df['x'], func(df['x'], *parameter), 'b-', label='fit', color='Blue')   # the star is to unpack the parameter array
print(parameter)
print(covariance_matrix)
print()
parameter, covariance_matrix = curve_fit(func, df['x'], df['seidel'])
plt.plot(df['x'], func(df['x'], *parameter), 'b-', label='fit', color='Red')   # the star is to unpack the parameter array
print(parameter)
print(covariance_matrix)
print()
parameter, covariance_matrix = curve_fit(func, df['x'], df['fast'])
plt.plot(df['x'], func(df['x'], *parameter), 'b-', label='fit', color='Green')   # the star is to unpack the parameter array
print(parameter)
print(covariance_matrix)
print()
plt.show()
