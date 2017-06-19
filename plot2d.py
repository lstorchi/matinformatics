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

fp = open(file)
hdr = fp.readline()

CLUST = 7

A = []
E = []
G = []
I = []
O = []
R = []
V = []
name = []
color = []
lX = []

initialcenter = numpy.zeros((CLUST,2))

for l in fp:
    line = l.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    lv = line.split(",")


    x = float(lv[7])
    y = float(lv[12])

    print x, y

    name.append(lv[0])
    if lv[1] == "A":
        color.append("yellow")
        A.append((x, y))
    elif lv[1] == "E":
        color.append("pink")
        E.append((x, y))
    elif lv[1] == "G":
        color.append("blue")
        G.append((x, y))
    elif lv[1] == "I":
        color.append("grey")
        I.append((x, y))
    elif lv[1] == "O":
        color.append("orange")
        O.append((x, y))
    elif lv[1] == "R":
        color.append("red")
        R.append((x, y))
    elif lv[1] == "V":
        color.append("green")
        V.append((x, y))

    lX.append([x, y])

fp.close()

initialcenter[0,:] = numpy.mean(A, axis=0)
initialcenter[1,:] = numpy.mean(E, axis=0)
initialcenter[2,:] = numpy.mean(G, axis=0)
initialcenter[3,:] = numpy.mean(I, axis=0)
initialcenter[4,:] = numpy.mean(O, axis=0)
initialcenter[5,:] = numpy.mean(R, axis=0)
initialcenter[6,:] = numpy.mean(V, axis=0)

print initialcenter

X = numpy.asarray(lX)

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
            

fig1, ax1 = matplotlib.pyplot.subplots()
ax1.scatter(X[:, 0], X[:, 1], c=color, s=100)
for i, txt in enumerate(name):
    ax1.annotate(txt, (X[i, 0], X[i, 1]))


fig2, ax2 = matplotlib.pyplot.subplots()
ax2.scatter(X[:, 0], X[:, 1], c=labels.astype(numpy.float), s=100)
for i, txt in enumerate(name):
    ax2.annotate(txt, (X[i, 0], X[i, 1]))

matplotlib.pyplot.show()
