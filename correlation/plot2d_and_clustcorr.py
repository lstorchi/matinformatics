import sys

import numpy 
import matplotlib.pyplot 
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

###############################################################################

def corrval (a1, a2):

  print "%4.2f "%(scipy.stats.pearsonr(a1, a2)[0]) + " P "

  a1m = numpy.mean(a1)
  a2m = numpy.mean(a2) 
  a1s = numpy.std(a1)
  a2s = numpy.std(a2)

  pcmp = 0.0
  for i in range(len(a1)):
      pcmp += (a1[i] - a1m)*(a2[i] - a2m)

  #print "P computed: ", pcmp/(len(a1)*a1s*a2s)

  print "%4.2f "%(scipy.stats.spearmanr(a1, a2)[0])+ " S"
  print "%4.2f "%(scipy.stats.kendalltau(a1, a2)[0])+ " K"

###############################################################################

def printcc (name, A, An):
    print name
    for n in An:
        sys.stdout.write(n + " ")
    print ""
    if (len(A) > 3):
        corrval(numpy.asarray(A)[:, 0], numpy.asarray(A)[:, 1])
        print ""

###############################################################################

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

An = []
En = []
Gn = []
In = []
On = []
Rn = []
Vn = []

lX = []
name = []
color = []

xnum = 8
ynum = 12
ynump = 13

initialcenter = numpy.zeros((CLUST,2))

for l in fp:
    line = l.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    lv = line.split(",")

    x = float(lv[xnum])
    y = float(lv[ynum]) + float(lv[ynump])

    name.append(lv[0])
    if lv[1] == "A":
        color.append("yellow")
        A.append((x, y))
        An.append(lv[0])
    elif lv[1] == "E":
        color.append("pink")
        E.append((x, y))
        En.append(lv[0])
    elif lv[1] == "G":
        color.append("blue")
        G.append((x, y))
        Gn.append(lv[0])
    elif lv[1] == "I":
        color.append("grey")
        I.append((x, y))
        In.append(lv[0])
    elif lv[1] == "O":
        color.append("orange")
        O.append((x, y))
        On.append(lv[0])
    elif lv[1] == "R":
        color.append("red")
        R.append((x, y))
        Rn.append(lv[0])
    elif lv[1] == "V":
        color.append("green")
        V.append((x, y))
        Vn.append(lv[0])

    lX.append([x, y])

fp.close()

initialcenter[0,:] = numpy.mean(A, axis=0)
printcc ("A", A, An)
initialcenter[1,:] = numpy.mean(E, axis=0)
printcc ("E", E, En)
initialcenter[2,:] = numpy.mean(G, axis=0)
printcc ("G", G, Gn)
initialcenter[3,:] = numpy.mean(I, axis=0)
printcc ("I", I, In)
initialcenter[4,:] = numpy.mean(O, axis=0)
printcc ("O", O, On)
initialcenter[5,:] = numpy.mean(R, axis=0)
printcc ("R", R, Rn)
initialcenter[6,:] = numpy.mean(V, axis=0)
printcc ("V", V, Vn)

#print initialcenter

X = numpy.asarray(lX)

est = KMeans(n_clusters=CLUST, init=initialcenter)
#est = KMeans(n_clusters=CLUST)

est.fit(X)
labels = est.labels_

x = set()

for i in labels:
    x.add(i)

for i in x:
    xc = []
    yc = []
    for j in range(len(labels)):
        if labels[j] == i:
            sys.stdout.write ("%s "%(name[j]))
            xc.append(X[j, 0])
            yc.append(X[j, 1])
    print ""
    if (len(xc) > 3):
      corrval(xc, yc)
      print ""
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
