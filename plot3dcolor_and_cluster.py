import sys

import numpy 
import matplotlib.pyplot 
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

from sklearn.cluster import KMeans

file = ""

if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " file "
    exit(1)

lX = []
color = []
name = []

fp = open(file)
hdr = fp.readline()

for l in fp:
    lv = l.split()

    name.append(lv[0])
    if lv[1] == "G":
        color.append("yellow")
    elif lv[1] == "R":
        color.append("pink")
    elif lv[1] == "B":
        color.append("blue")
    elif lv[1] == "I":
        color.append("grey")
    elif lv[1] == "A":
        color.append("orange")
    elif lv[1] == "V":
        color.append("green")
    elif lv[1] == "L":
        color.append("white")
    elif lv[1] == "O":
        color.append("red")

    lX.append([float(lv[2]), float(lv[3]), float(lv[4])])

fp.close()

X = numpy.asarray(lX)

est = KMeans(n_clusters=8)


est.fit(X)
labels = est.labels_

x = set()

for i in labels:
    x.add(i)

for i in x:
    for j in range(len(labels)):
        if labels[j] == i:
            sys.stdout.write ("%s "%(name[j]))
    print ""
            

fig = matplotlib.pyplot.figure(1, figsize=(4, 3))
matplotlib.pyplot.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
matplotlib.pyplot.cla()
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, s=100)
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('GM2-')
ax.set_ylabel('GM5+')
ax.set_zlabel('M2-')

fig = matplotlib.pyplot.figure(2, figsize=(4, 3))
matplotlib.pyplot.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
matplotlib.pyplot.cla()
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(numpy.float), s=100)
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('GM2-')
ax.set_ylabel('GM5+')
ax.set_zlabel('M2-')

matplotlib.pyplot.show()


