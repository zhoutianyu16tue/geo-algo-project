import matplotlib.pyplot as plt
from pandas import DataFrame

df = DataFrame()

with open('sweep2000.txt', 'r') as fd:
    lines = fd.readlines()

sweep = []

for line in lines:
    sweep.append(float(line))


with open('seidel2000.txt', 'r') as fd:
    lines = fd.readlines()

seidel = []

for line in lines:
    seidel.append(float(line))

df['x'] = range(100, 2100, 100)
df['sweep'] = sweep
df['seidel'] = seidel

ax = df.plot(kind='scatter', x='x', y='seidel',color='Red');
df.plot(kind='scatter', x='x', y='sweep',color='Blue', ax=ax);
plt.show()