from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data_file = 'data/polcompass.csv'

stances = {'libleft': 'g',
        'libright': 'y',
        'authleft': 'r',
        'authright': 'b',
        'centrist': '#c9c1c1',
        'libright2': 'm',
        'None': 'k',
        'left': '#71e827',
        'right': '#5c8d91',
        'lib': '#4c824a',
        'auth': '#7b34ad'}

with open(data_file, 'r') as f:
    reader = csv.reader(f)

    users = defaultdict(list)
    for row in reader:
        ts, id, name, leaning = row
        users[name].append((int(ts), leaning))


snapshots_ts = list(range(1570491626, max(v[0][0] for v in users.values()), 10000))
series = {stance: [v[0][0] for v in users.values() if v[-1][1] == stance]
            for stance in stances}
cdf = {stance: np.cumsum(np.histogram(series[stance], bins=snapshots_ts)[0])
            for stance in stances}

M = np.array([[cdf['libleft'],   cdf['left'],  cdf['lib'],  cdf['centrist']],
                [cdf['libright'],  cdf['right'], cdf['lib'],  cdf['centrist']],
                [cdf['authleft'],  cdf['left'],  cdf['auth'], cdf['centrist']],
                [cdf['authright'], cdf['right'], cdf['auth'], cdf['centrist']]])
M[1, 0] += cdf['libright2']
# Kinda like the dot product across axis=1
y = np.einsum('ijk,j->ik', M, np.array([1, 0.5, 0.5, 0.25]))

fig, ax = plt.subplots()
ax.stackplot(np.array(snapshots_ts, dtype='datetime64[s]')[1:], y / np.linalg.norm(y, axis=0, ord=1),
                labels=['libleft', 'libright', 'authleft', 'authright'],
                colors=['g', 'y', 'r', 'b'])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.set_ylabel('% of users')

fig2, ax2 = plt.subplots()
for stance, color in stances.items():
    ax2.plot(np.array(series[stance], dtype='datetime64[s]'), range(1, len(series[stance]) + 1), color=color, label=stance)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.set_ylabel('Cumulative # of users')
ax2.legend()
plt.show()
