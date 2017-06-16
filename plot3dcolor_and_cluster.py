import sys

import numpy 
import matplotlib.pyplot 
from mpl_toolkits.mplot3d import Axes3D
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

CLUST = 8

fp = open(file)
hdr = fp.readline()

initialcenter = numpy.zeros((CLUST,3))

G = []
R = []
B = []
I = []
A = []
V = []
L = []
O = []

for l in fp:
    lv = l.split()

    x = float(lv[2])
    y = float(lv[3])
    z = float(lv[4])

    name.append(lv[0])
    if lv[1] == "G":
        color.append("yellow")
        G.append((x, y, z))
    elif lv[1] == "R":
        color.append("pink")
        R.append((x, y, z))
    elif lv[1] == "B":
        color.append("blue")
        B.append((x, y, z))
    elif lv[1] == "I":
        color.append("grey")
        I.append((x, y, z))
    elif lv[1] == "A":
        color.append("orange")
        A.append((x, y, z))
    elif lv[1] == "V":
        color.append("green")
        V.append((x, y, z))
    elif lv[1] == "L":
        color.append("white")
        L.append((x, y, z))
    elif lv[1] == "O":
        color.append("red")
        O.append((x, y, z))

    lX.append([x, y, z])

fp.close()

initialcenter[0,:] = numpy.mean(G, axis=0)
initialcenter[1,:] = numpy.mean(R, axis=0)
initialcenter[2,:] = numpy.mean(B, axis=0)
initialcenter[3,:] = numpy.mean(I, axis=0)
initialcenter[4,:] = numpy.mean(A, axis=0)
initialcenter[5,:] = numpy.mean(V, axis=0)
initialcenter[6,:] = numpy.mean(L, axis=0)
initialcenter[7,:] = numpy.mean(O, axis=0)

print initialcenter

X = numpy.asarray(lX)
#print X

est = KMeans(n_clusters=CLUST, init=initialcenter)

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
for i, txt in enumerate(name):
    ax.text(X[i,0],X[i,1],X[i, 2], txt)
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
for i, txt in enumerate(name):
    ax.text(X[i,0], X[i,1], X[i, 2], txt)
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('GM2-')
ax.set_ylabel('GM5+')
ax.set_zlabel('M2-')

matplotlib.pyplot.show()
