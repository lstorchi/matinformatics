import sys

import scipy
import numpy 
import matplotlib.pyplot 
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

lX = []
color = []
name = []

CLUST = 7

fp = open(file)
hdr = fp.readline()

initialcenter = numpy.zeros((CLUST,3))

A = []
E = []
G = []
I = []
O = []
R = []
V = []

Adesw = []
Edesw = []
Gdesw = []
Idesw = []
Odesw = []
Rdesw = []
Vdesw = []

Adeplus = []
Edeplus = []
Gdeplus = []
Ideplus = []
Odeplus = []
Rdeplus = []
Vdeplus = []

desw = []
deplus = []

y1num = 12
y2num = 13

for l in fp:
    line = l.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    lv = line.split(",")

    x = float(lv[7])
    y = float(lv[8])
    z = float(lv[9])

    y1 = float(lv[y1num])
    y2 = float(lv[y2num])

    desw.append(y1)
    deplus.append(y1 + y2)

    #print x, y, z

    name.append(lv[0])
    if lv[1] == "A":
        color.append("yellow")
        A.append((x, y, z))
        Adesw.append(y1)
        Adeplus.append(y1 + y2)
    elif lv[1] == "E":
        color.append("pink")
        E.append((x, y, z))
        Edesw.append(y1)
        Edeplus.append(y1 + y2) 
    elif lv[1] == "G":
        color.append("blue")
        G.append((x, y, z))
        Gdesw.append(y1)
        Gdeplus.append(y1 + y2) 
    elif lv[1] == "I":
        color.append("grey")
        I.append((x, y, z))
        Idesw.append(y1)
        Ideplus.append(y1 + y2)
    elif lv[1] == "O":
        color.append("orange")
        O.append((x, y, z))
        Odesw.append(y1)
        Odeplus.append(y1 + y2)
    elif lv[1] == "R":
        color.append("red")
        R.append((x, y, z))
        Rdesw.append(y1)
        Rdeplus.append(y1 + y2)
    elif lv[1] == "V":
        color.append("green")
        V.append((x, y, z))
        Vdesw.append(y1)
        Vdeplus.append(y1 + y2)

    lX.append([x, y, z])

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
#print X

est = KMeans(n_clusters=CLUST, init=initialcenter)

est.fit(X)
labels = est.labels_

x = set()

for i in labels:
    x.add(i)

for i in x:
    x1 = []
    clustdesw = []

    x2 = []
    clustdeplus = []

    for j in range(len(labels)):
        if labels[j] == i:
            x1.append(lX[j][0])
            clustdesw.append(desw[j])

            x2.append(lX[j][1])
            clustdeplus.append(deplus[j])
            sys.stdout.write ("%s "%(name[j]))

    if (len(x1) > 3):
      print ""
      print "DEsw"
      corrval(x1, clustdesw)
      print "DEsw + De"
      corrval(x2, clustdeplus)
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
