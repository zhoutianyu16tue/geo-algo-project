import matplotlib.pyplot as plt
from pandas import DataFrame

df = DataFrame()
numOfSet = 5100
df['x'] = range(100, numOfSet, 100)
files = ['sweep', 'seidel', 'fast']
data = [[],[],[]]

for idx, file in enumerate(files):
    with open(file + '5000.txt', 'r') as fd:
        lines = fd.readlines()

    for line in lines:
        data[idx].append(float(line))


df['sweep'] = data[0]
df['seidel'] = data[1]
df['fast'] = data[2]

ax = df.plot(kind='scatter', x='x', y='seidel',color='Red');
df.plot(kind='scatter', x='x', y='sweep',color='Blue', ax=ax);
df.plot(kind='scatter', x='x', y='fast',color='Black', ax=ax);
plt.show()