import sys

import math 
import numpy 
import matplotlib.pyplot 
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

import utils

###############################################################################

def compute_and_print_corr (x, dv, dvov, desw, de, deswpde, p):

    dvP, dvS, dvK = utils.corrval(numpy.asarray(x), numpy.asarray(dv))
    dvovP, dvovS, dvovK = utils.corrval(numpy.asarray(x), numpy.asarray(dvov))
    deswP, deswS, deswK = utils.corrval(numpy.asarray(x), numpy.asarray(desw))
    deP, deS, deK = utils.corrval(numpy.asarray(x), numpy.asarray(de))
    deswpdeP, deswpdeS, deswpdeK = utils.corrval(numpy.asarray(x), numpy.asarray(deswpde))
    xn = []
    pn = []
    for i in range(len(p)):
        if not math.isnan(p[i]):
            xn.append(x[i])
            pn.append(p[i])

    pP, pS, pK = utils.corrval(numpy.asarray(xn), numpy.asarray(pn))

    sys.stdout.write(" %5.2f P , %5.2f P , "%(dvP, dvovP))
    sys.stdout.write(" %5.2f P , %5.2f P , "%(deswP, deP))
    sys.stdout.write(" %5.2f P , %5.2f P \n "%(deswpdeP, pP))

    sys.stdout.write(" %5.2f S , %5.2f S , "%(dvS, dvovS))
    sys.stdout.write(" %5.2f S , %5.2f S , "%(deswS, deS))
    sys.stdout.write(" %5.2f S , %5.2f S \n "%(deswpdeS, pS))

    sys.stdout.write(" %5.2f K , %5.2f K , "%(dvK, dvovK))
    sys.stdout.write(" %5.2f K , %5.2f K , "%(deswK, deK))
    sys.stdout.write(" %5.2f K , %5.2f K \n "%(deswpdeK, pK))
 
    print ""

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

colors_map = {"A": "#DC143C", \
        "E" : "#FF00FF", \
        "G" : "#7D26CD", \
        "I" : "#4169E1", \
        "O" : "#00BFFF", \
        "R" : "#00C78C", \
        "V" : "#FFFF00", \
        "B" : "#EE7600"}

file = ""

if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " file "
    exit(1)

fp = open(file)
hdr = fp.readline()

gm2 = []
gm5 = []
m2 = []
dv = []
dvov = []
desw = []
de = []
p = []
desw_p_de = []
names = []
classes = []
colors = []

setofclasses = set()

linenum = 2
for l in fp:
    line = l.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    lv = line.split(",")

    if len (lv)!= 15:
        print "Error at line ", linenum 
        exit(1) 

    linenum += 1

    gm2.append(float(lv[7])) 
    gm5.append(float(lv[8]))
    m2.append(float(lv[9]))

    dv.append(float(lv[10]))
    dvov.append(float(lv[11]))
    desw.append(float(lv[12]))
    de.append(float(lv[13]))
    if (utils.is_number(lv[14])):
        p.append(float(lv[14]))
    else:
        p.append(float("nan"))

    desw_p_de.append(float(lv[12]) + float(lv[13]))

    names.append(lv[0])
    classes.append(lv[1])

    setofclasses.add(lv[1])

    if not (lv[1] in colors_map.keys()):
        print "Error at line ", linenum, \
                " color not defined for the give key ", lv[1]
        exit(1)

    colors.append(colors_map[lv[1]])


fp.close()

print "Correlation GM2-"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
compute_and_print_corr (gm2, dv, dvov, desw, de, desw_p_de, p)
print ""

print "Correlation GM5+"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
compute_and_print_corr (gm5, dv, dvov, desw, de, desw_p_de, p)
print ""

print "Correlation M2-"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
compute_and_print_corr (m2, dv, dvov, desw, de, desw_p_de, p)
print ""




exit(1)


printcc ("A", A, An)
printcc ("E", E, En)
printcc ("G", G, Gn)
printcc ("I", I, In)
printcc ("O", O, On)
printcc ("R", R, Rn)
printcc ("V", V, Vn)

lX.append([x, y])

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
