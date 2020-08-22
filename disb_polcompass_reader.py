import math
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties

data_file = 'assets\\reddit\\polcompass\\polcompass.csv'

with open(data_file) as f:
    reader = csv.reader(f)

    users, ids = {}, {}
    for row in reader:
        users[row[2]] = row[3]
        ids[row[1]] = row[3]

#stances_dict = {stance: len([u for u, s in users.items() if s == stance]) for stance in stances}
stances_dict, ids_dict = {}, {}
stances = {s for u, s in users.items()}
for stance in stances:
    ids_dict[stance] = len([c for c, s in ids.items() if s == stance])
    stances_dict[stance] = len([u for u, s in users.items() if s == stance])
    print('%s: %d, %d, %.2f' % (stance, stances_dict[stance], ids_dict[stance], ids_dict[stance]/stances_dict[stance]))
print('total: %d, %d, %.2f' % (len(users), len(ids), len(ids)/len(users)))

libleft = stances_dict['libleft'] + 0.5*stances_dict['left'] + 0.5*stances_dict['lib'] + 0.25*stances_dict['centrist']
libright = stances_dict['libright'] + 0.5*stances_dict['right'] + 0.5*stances_dict['lib'] + 0.25*stances_dict['centrist'] + stances_dict['libright2']
authleft = stances_dict['authleft'] + 0.5*stances_dict['left'] + 0.5*stances_dict['auth'] + 0.25*stances_dict['centrist']
authright = stances_dict['authright'] + 0.5*stances_dict['right'] + 0.5*stances_dict['auth'] + 0.25*stances_dict['centrist']
total = libleft + libright + authleft + authright

fig, ax = plt.subplots(1)
params = {'bottom':False, 'top':False, 'labelbottom':False, 'right':False, 'left':False, 'labelleft':False}
plt.tick_params(axis='both', which='both', **params)

quads = [(authright, (1,1), 'b', 'authright'),
        (libright, (1,-1), 'y', 'libright'),
        (authleft, (-1,1), 'r', 'authleft'),
        (libleft, (-1,-1), 'g', 'libleft')]

for followers, loc, clr, leaning in quads:
    rect = patches.Rectangle((0,0),loc[0]*math.sqrt(followers),loc[1]*math.sqrt(followers),linewidth=1,edgecolor=clr,facecolor=clr,alpha=0.6)
    ax.add_patch(rect)
    ax.annotate(s=str(round(followers)) + '\n(' + str(round(100*followers/total)) + '%)',
                    xy=(0.5*loc[0]*math.sqrt(followers),0.5*loc[1]*math.sqrt(followers)), fontsize=0.2*math.sqrt(followers), alpha=1,
                    xycoords='data', verticalalignment='center',
                    horizontalalignment='center' , color=clr)

labels= [('Economic- \n Left', (0.02,0.5), 'center', 'left'),
        ('Economic- \n Right', (0.98,0.5), 'center', 'right'),
        ('Authoritarian', (0.5,0.98), 'top', 'center'),
        ('Libertarian', (0.5,0.02), 'bottom', 'center')]
for label, loc, valn, haln in labels:
    ax.annotate(s=label, xy=loc, fontsize=12, alpha=1,
                        xycoords='axes fraction', verticalalignment=valn,
                        horizontalalignment=haln , color='k')

prop = FontProperties(family='consolas', style='normal')
ax.annotate(s='u/tigeer', xy=(0.99,0.01), fontsize=12, alpha=0.8, fontproperties=prop,
                    xycoords='axes fraction', verticalalignment='bottom',
                    horizontalalignment='right' , color='#999999')

plt.axhline(0, color='k', ls='-', linewidth=1)
plt.axvline(0, color='k', ls='-', linewidth=1)

l = math.sqrt(max([q[0] for q in quads]))
ax.axis([-1*l,l,-1*l,l])
ax.set_aspect('equal', 'box')
plt.title('What are the views of\nr/PoliticalCompassMemes users\n(by user flair)', fontsize=18)
#The political compass, scaled to reflect the views of r/PoliticalCompassMemes users [OC]
plt.tight_layout()
plt.show()
