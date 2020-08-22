import numpy as np
import csv
import matplotlib.pyplot as plt
from bisect import bisect_left

data_file = 'assets\\reddit\\polcompass\\polcompass.csv'

with open(data_file) as f:
    reader = csv.reader(f)

    users = {}
    for row in reader:
        ts, name, leaning = int(row[0]), row[2], row[3]
        if name not in users: users[name] = []
        users[name].append((ts, leaning))

stances = {s[-1][1] for u, s in users.items()}

series = {}
for stance in stances:
    series[stance] = [s[0][0] for u, s in users.items() if s[-1][1] == stance]


def take_snapshot(t):
    def b(stance, time=t):
        return bisect_left(series[stance], t)
    libleft = b('libleft') + 0.5*b('left') + 0.5*b('lib') + 0.25*b('centrist')
    libright = b('libright') + 0.5*b('right') + 0.5*b('lib') + 0.25*b('centrist') + b('libright2')
    authleft = b('authleft') + 0.5*b('left') + 0.5*b('auth') + 0.25*b('centrist')
    authright = b('authright') + 0.5*b('right') + 0.5*b('auth') + 0.25*b('centrist')
    return [libleft, libright, authleft, authright]

norm = lambda a: list(map(lambda x: x/sum(a) if sum(a) != 0 else 0, a))

snapshots_ts = list(range(1570491626, max(s[0][0] for u, s in users.items()), 10000))
y = [norm(take_snapshot(ts)) for ts in snapshots_ts]

fig, ax = plt.subplots(1)
plt.stackplot(snapshots_ts, np.transpose(y),
                labels=['libleft', 'libright', 'authleft', 'authright'],
                colors=['g', 'y', 'r', 'b'])

fig2, ax2 = plt.subplots(1)
tracks = [('libleft', 'g'),
        ('libright', 'y'),
        ('authleft', 'r'),
        ('authright', 'b'),
        ('centrist', '#c9c1c1'),
        ('libright2', 'm'),
        ('None', 'k'),
        ('left', '#71e827'),
        ('right', '#5c8d91'),
        ('lib', '#4c824a'),
        ('auth', '#7b34ad')]

for track, clr in tracks:
    plt.plot(series[track], range(1, len(series[track]) + 1), color=clr, label=track)
plt.legend()
plt.show()
