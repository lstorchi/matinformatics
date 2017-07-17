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
parser.add_argument("-s","--show", help="display all scatter plots", \
        required=False, default=False, action="store_true")
parser.add_argument("-c","--cshow", help="display all scatter plots for a "\
        "specific cluster", \
        required=False, default="", type=str)


if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

file = args.file

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

allx = []

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

    if not (lv[1] in utils.colors_map.keys()):
        print "Error at line ", linenum, \
                " color not defined for the give key ", lv[1]
        exit(1)

    colors.append(utils.colors_map[lv[1]])

    allx.append([gm2[-1], gm5[-1], m2[-1]])

fp.close()

numofclust = len(setofclasses)
initialcenter = numpy.zeros((numofclust, 3))

cn = 0
for c in setofclasses:

    s_allx = []
    for i in range(len(classes)):
        
        if (classes[i] == c):
            s_allx.append([gm2[i], gm5[i], m2[i]])
        
    initialcenter[cn,:] = numpy.mean(s_allx, axis=0)
    cn += 1


X = numpy.asarray(allx)

est = KMeans(n_clusters=numofclust, init=initialcenter)
est.fit(X)
labels = est.labels_

x = set()
for i in labels:
    x.add(i)

for i in x:

    print "Selected cluster ", i

    s_gm2 = []
    s_gm5 = []
    s_m2 = []

    s_dv = []
    s_dvov = []
    s_desw = []
    s_de = []
    s_p = []
    s_desw_p_de = []
    s_names = []

    #not used now
    s_classes = []
    s_colors = []

    for j in range(len(labels)):
        if labels[j] == i:
            s_gm2.append(gm2[j])
            s_gm5.append(gm5[j])
            s_m2.append(m2[j])

            s_dv.append(dv[j])
            s_dvov.append(dvov[j])
            s_desw.append(desw[j])

            s_de.append(de[j])
            s_p.append(p[j])
            s_desw_p_de.append(desw_p_de[j])

            s_names.append(names[j])
            s_classes.append(classes[j])
            s_colors.append(colors[j])

    if args.cshow != "":
        if int(args.cshow) == i:
            pltplot(s_gm2, "GM2-", s_dv, "DV", s_names , "GM2- vs DV")
            pltplot(s_gm2, "GM2-", s_dvov, "DV/V", s_names, "GM2- vs DV/V")
            pltplot(s_gm2, "GM2-", s_desw, "DESW", s_names, "GM2- vs DESW")
            pltplot(s_gm2, "GM2-", s_de, "DE", s_names, "GM2- vs DE")
            pltplot(s_gm2, "GM2-", s_desw_p_de, "DESW + DE", s_names, "GM2- vs DDESW + DE")
            
            lp = []
            lgm2 = []
            lnames = []
            for i in range(len(s_p)):
                if not math.isnan(s_p[i]):
                    lp.append(s_p[i])
                    lgm2.append(s_gm2[i])
                    lnames.append(s_names[i])
                    
            pltplot(lgm2, "GM2-", lp, "P", lnames, "GM2- vs P")
            
            pltplot(s_gm5, "GM5+", s_dv, "DV", s_names, "GM5+ vs DV")
            pltplot(s_gm5, "GM5+", s_dvov, "DV/V", s_names, "GM5+ vs DV/V")
            pltplot(s_gm5, "GM5+", s_desw, "DESW", s_names, "GM5+ vs DESW")
            pltplot(s_gm5, "GM5+", s_de, "DE", s_names, "GM5+ vs DE")
            pltplot(s_gm5, "GM5+", s_desw_p_de, "DESW + DE", s_names, "GM5+ vs DDESW + DE")
            
            lp = []
            lgm5 = []
            lnames = []
            for i in range(len(s_p)):
                if not math.isnan(s_p[i]):
                    lp.append(s_p[i])
                    lgm5.append(s_gm5[i])
                    lnames.append(s_names[i])
                    
            pltplot(lgm5, "GM5+", lp, "P", lnames, "GM5+ vs P")
            
            pltplot(s_m2, "M2-", s_dv, "DV", s_names, "M2- vs DV")
            pltplot(s_m2, "M2-", s_dvov, "DV/V", s_names, "M2- vs DV/V")
            pltplot(s_m2, "M2-", s_desw, "DESW", s_names, "M2- vs DESW")
            pltplot(s_m2, "M2-", s_de, "DE", s_names, "M2- vs DE")
            pltplot(s_m2, "M2-", s_desw_p_de, "DESW + DE", s_names, "M2- vs DDESW + DE")
            
            lp = []
            lm2 = []
            lnames = []
            for i in range(len(s_p)):
                if not math.isnan(s_p[i]):
                    lp.append(s_p[i])
                    lm2.append(s_gm5[i])
                    lnames.append(s_names[i])
                    
            pltplot(lm2, "M2-", lp, "P", lnames, "M2- vs P")

    if (len(s_names) >= utils.LIMITNUMOF):
        sys.stdout.write("class dim %d ,"%(len(s_names) ))
        for n in s_names:
            sys.stdout.write("%s "%(n))
        sys.stdout.write("\n")

        print "Correlation GM2-"
        print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
        utils.compute_and_print_corr (s_gm2, s_dv, s_dvov, s_desw, s_de, s_desw_p_de, s_p)
        
        print "Correlation GM5+"
        print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
        utils.compute_and_print_corr (s_gm5, s_dv, s_dvov, s_desw, s_de, s_desw_p_de, s_p)
        
        print "Correlation M2-"
        print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
        utils.compute_and_print_corr (s_m2, s_dv, s_dvov, s_desw, s_de, s_desw_p_de, s_p)

if args.show:

    fig = matplotlib.pyplot.figure(1, figsize=(4, 3))
    matplotlib.pyplot.clf()
    fig.suptitle("Initial cluster")
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    matplotlib.pyplot.cla()
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=colors, s=100)
    for i, txt in enumerate(names):
        ax.text(X[i,0],X[i,1],X[i, 2], txt)
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('GM2-')
    ax.set_ylabel('GM5+')
    ax.set_zlabel('M2-')
    
    fig = matplotlib.pyplot.figure(2, figsize=(4, 3))
    matplotlib.pyplot.clf()
    fig.suptitle("Kmeans2")
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    matplotlib.pyplot.cla()
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(numpy.float), s=100)
    for i, txt in enumerate(names):
        ax.text(X[i,0], X[i,1], X[i, 2], txt)
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('GM2-')
    ax.set_ylabel('GM5+')
    ax.set_zlabel('M2-')
    
if args.show or args.cshow != "":
    matplotlib.pyplot.show()
