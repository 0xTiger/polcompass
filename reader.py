import math
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties
from collections import Counter

data_file = 'data/polcompass.csv'

with open(data_file) as f:
    reader = csv.reader(f)

    users, ids = {}, {}
    for row in reader:
        ts, id, name, leaning = row
        users[name] = leaning
        ids[id] = leaning

stances = set(users.values())
comment_stance_counts = Counter(ids.values())
user_stance_counts = Counter(users.values())

print(f'{"":<10}: users, comments, comments/user')
for stance in stances:
    print(f'{stance:<10}: {user_stance_counts[stance]}, {comment_stance_counts[stance]}, {comment_stance_counts[stance]/user_stance_counts[stance]:.2f}')
print(f'{"total":<10}: {len(users)}, {len(ids)}, {len(ids)/len(users):.2f}')

libleft = user_stance_counts['libleft'] + 0.5*user_stance_counts['left'] + 0.5*user_stance_counts['lib'] + 0.25*user_stance_counts['centrist']
libright = user_stance_counts['libright'] + 0.5*user_stance_counts['right'] + 0.5*user_stance_counts['lib'] + 0.25*user_stance_counts['centrist'] + user_stance_counts['libright2']
authleft = user_stance_counts['authleft'] + 0.5*user_stance_counts['left'] + 0.5*user_stance_counts['auth'] + 0.25*user_stance_counts['centrist']
authright = user_stance_counts['authright'] + 0.5*user_stance_counts['right'] + 0.5*user_stance_counts['auth'] + 0.25*user_stance_counts['centrist']
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
    ax.annotate(s=f'{round(followers)}\n({round(100*followers/total)}%)',
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
