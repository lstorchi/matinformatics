import sys

import scipy
import numpy 
import argparse
import math

import matplotlib.pyplot 
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

import utils

###############################################################################

def pltplot(x, xl, y, yl, names, title):

    fig1, ax1 = matplotlib.pyplot.subplots()
    ax1.scatter(x, y, c=colors, s=100)
    fig1.suptitle(title)
    matplotlib.pyplot.xlabel(xl)
    matplotlib.pyplot.ylabel(yl)
    for i, txt in enumerate(names):
        ax1.annotate(txt, (x[i], y[i]))

###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="input csv file ", \
        required=True, type=str)
parser.add_argument("-p","--showscatterplot", help="Show scatter plot for rows n, m and p \"n,m,p\" "\
        "start numbering from 0", required=True, default="", type=str)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

filename = args.file

columnum = args.showscatterplot

line = columnum.replace(" ", "")
line = line.replace("\t", "")
line = line.replace("\n", "")
columnum = line.split(",")

if len(columnum) != 3:
    print "Error three colum required"
    exit(1)

xnum = int(columnum[0])
ynum = int(columnum[1])
znum = int(columnum[2])

fp = open(filename)
hdr = fp.readline()

line = hdr.replace(" ", "")
line = line.replace("\t", "")
line = line.replace("\n", "")
hdr = line.split(",")

if (xnum >= len (hdr)) or (ynum >= len (hdr)):
    print "Wrong column specified ", linenum
    exit(1)

xname = hdr[xnum]
yname = hdr[ynum]
zname = hdr[znum]

xall = []
yall = []
zall = []
names = []
classes = []
colors = []
allx = []

setofclasses = set()

linenum = 2
for l in fp:
    line = l.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    lv = line.split(",")

    if len (lv) < 4:
        print "Error at line ", linenum 
        exit(1) 

    if (xnum >= len (lv)) or (ynum >= len (lv)) \
            or (znum >= len (lv)):
        print "Error at line ", linenum
        exit(1)

    linenum += 1
   
    if (lv[1] != "X"):
        if utils.is_number(lv[xnum]) and utils.is_number(lv[ynum]):
            xall.append(float(lv[xnum]))
            yall.append(float(lv[ynum]))
            zall.append(float(lv[znum]))
            names.append(lv[0]+ " ("+lv[1]+")")
            classes.append(lv[1])
            setofclasses.add(lv[1])

            if not (lv[1] in utils.colors_map.keys()):
                print "Error at line ", linenum, \
                    " color not defined for the give key ", lv[1]
                exit(1)

            colors.append(utils.colors_map[lv[1]])

            allx.append([xall[-1], yall[-1], zall[-1]])

fp.close()

numofclust = len(setofclasses)
initialcenter = numpy.zeros((numofclust, 3))

cn = 0
for c in setofclasses:

    s_allx = []
    for i in range(len(classes)):
        
        if (classes[i] == c):
            s_allx.append([xall[i], yall[i], zall[i]])
        
    initialcenter[cn,:] = numpy.mean(s_allx, axis=0)
    cn += 1


X = numpy.asarray(allx)

est = KMeans(n_clusters=numofclust, init=initialcenter)
est.fit(X)
labels = est.labels_

if args.showscatterplot != "":

    fig = matplotlib.pyplot.figure(1, figsize=(4, 3))
    matplotlib.pyplot.clf()
    fig.suptitle("Initial cluster")
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    matplotlib.pyplot.cla()
    ax.scatter(xall, yall, zall, c=colors, s=100)
    for i, txt in enumerate(names):
        ax.text(xall[i], yall[i], zall[i], txt)
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    ax.set_zlabel(zname)
    
    fig = matplotlib.pyplot.figure(2, figsize=(4, 3))
    matplotlib.pyplot.clf()
    fig.suptitle("Kmeans2")
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    matplotlib.pyplot.cla()
    ax.scatter(xall, yall, zall, c=labels.astype(numpy.float), s=100)
    for i, txt in enumerate(names):
        ax.text(xall[i], yall[i], zall[i], txt)
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    ax.set_zlabel(zname)
    
if args.showscatterplot != "" :
    matplotlib.pyplot.show()

