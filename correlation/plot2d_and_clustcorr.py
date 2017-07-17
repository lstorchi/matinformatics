import sys

import math 
import numpy 
import argparse

import scipy.stats
import matplotlib.pyplot 
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

import utils

###############################################################################

def pltplot(ax, axl, ay, ayl, anames, acolors):

    title = axl + "vs " + ayl
    fig1, ax1 = matplotlib.pyplot.subplots()
    ax1.scatter(ax, ay, c=acolors, s=100)
    fig1.suptitle(title)
    matplotlib.pyplot.xlabel(axl)
    matplotlib.pyplot.ylabel(ayl)
    for i, txt in enumerate(anames):
        ax1.annotate(txt, (ax[i], ay[i]))

###############################################################################

def add_all_plots (x, xname, yall, yname, allcolors, allnames):

    for i in range(len(yall)):

        y = yall[i]

        lx = []
        ly = []
        lnames = []
        lcolors = []
        for j in range(len(y)):
            if not math.isnan(y[j]):
                lx.append(x[j])
                ly.append(y[j])
                lnames.append(allnames[j])
                lcolors.append(allcolors[j])

        pltplot(lx, xname[i], ly, yname[i], lnames, lcolors)
 
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

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="input csv file ", \
        required=True, type=str)
parser.add_argument("-s","--show", help="display all scatter plots", \
        required=False, default=False, action="store_true")
parser.add_argument("-c","--cshow", help="display all scatter plots for a "\
        "specific class", \
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


fp.close()

print "Correlation GM2-"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
utils.compute_and_print_corr (gm2, dv, dvov, desw, de, desw_p_de, p)

print "Correlation GM5+"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
utils.compute_and_print_corr (gm5, dv, dvov, desw, de, desw_p_de, p)

print "Correlation M2-"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
utils.compute_and_print_corr (m2, dv, dvov, desw, de, desw_p_de, p)

for c in setofclasses:
    print "Selected class ", c

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

    for i in range(len(classes)):
        if (classes[i] == c):
            s_gm2.append(gm2[i])
            s_gm5.append(gm5[i])
            s_m2.append(m2[i])

            s_dv.append(dv[i])
            s_dvov.append(dvov[i])
            s_desw.append(desw[i])

            s_de.append(de[i])
            s_p.append(p[i])
            s_desw_p_de.append(desw_p_de[i])

            s_names.append(names[i])
            s_classes.append(classes[i])
            s_colors.append(colors[i])

    if args.cshow == c:
        pltplot(s_gm2, "GM2-", s_dv, "DV", s_names, s_colors)
        pltplot(s_gm2, "GM2-", s_dvov, "DV/V", s_names, s_colors)
        pltplot(s_gm2, "GM2-", s_desw, "DESW", s_names, s_colors)
        pltplot(s_gm2, "GM2-", s_de, "DE", s_names, s_colors)
        pltplot(s_gm2, "GM2-", s_desw_p_de, "DESW + DE", s_names, s_colors)

        lp = []
        lgm2 = []
        lnames = []
        lcolors = []
        for i in range(len(s_p)):
            if not math.isnan(s_p[i]):
                lp.append(s_p[i])
                lgm2.append(s_gm2[i])
                lnames.append(s_names[i])
                lcolors.append(s_colors[i])
                
        pltplot(lgm2, "GM2-", lp, "P", lnames, lcolors)
 
        pltplot(s_gm5, "GM5+", s_dv, "DV", s_names, s_colors)
        pltplot(s_gm5, "GM5+", s_dvov, "DV/V", s_names, s_colors)
        pltplot(s_gm5, "GM5+", s_desw, "DESW", s_names, s_colors)
        pltplot(s_gm5, "GM5+", s_de, "DE", s_names, s_colors)
        pltplot(s_gm5, "GM5+", s_desw_p_de, "DESW + DE", s_names, s_colors)

        lp = []
        lgm5 = []
        lnames = []
        lcolors = []
        for i in range(len(s_p)):
            if not math.isnan(s_p[i]):
                lp.append(s_p[i])
                lgm5.append(s_gm5[i])
                lnames.append(s_names[i])
                lcolors.append(s_colors[i])
                
        pltplot(lgm5, "GM5+", lp, "P", lnames, lcolors)
        
        pltplot(s_m2, "M2-", s_dv, "DV", s_names, s_colors)
        pltplot(s_m2, "M2-", s_dvov, "DV/V", s_names, s_colors)
        pltplot(s_m2, "M2-", s_desw, "DESW", s_names, s_colors)
        pltplot(s_m2, "M2-", s_de, "DE", s_names, s_colors)
        pltplot(s_m2, "M2-", s_desw_p_de, "DESW + DE", s_names, s_colors)

        lp = []
        lm2 = []
        lnames = []
        lcolors = []
        for i in range(len(s_p)):
            if not math.isnan(s_p[i]):
                lp.append(s_p[i])
                lm2.append(s_gm5[i])
                lnames.append(s_names[i])
                lcolors.append(s_colors[i])
                
        pltplot(lm2, "M2-", lp, "P", lnames, lcolors)

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
    pltplot(gm2, "GM2-", dv, "DV", names, colors)
    pltplot(gm2, "GM2-", dvov, "DV/V", names, colors)
    pltplot(gm2, "GM2-", desw, "DESW", names, colors)
    pltplot(gm2, "GM2-", de, "DE", names, colors)
    pltplot(gm2, "GM2-", desw_p_de, "DESW + DE", names, colors)
    
    lp = []
    lgm2 = []
    lnames = []
    lcolors = []
    for i in range(len(p)):
        if not math.isnan(p[i]):
            lp.append(p[i])
            lgm2.append(gm2[i])
            lnames.append(names[i])
            lcolors.append(colors[i])

    pltplot(lgm2, "GM2-", lp, "P", lnames)
    
    pltplot(gm5, "GM5+", dv, "DV", names, colors)
    pltplot(gm5, "GM5+", dvov, "DV/V", names, colors)
    pltplot(gm5, "GM5+", desw, "DESW", names, colors)
    pltplot(gm5, "GM5+", de, "DE", names, colors)
    pltplot(gm5, "GM5+", desw_p_de, "DESW + DE", names, colors)

    lp = []
    lgm5 = []
    lnames = []
    lcolors = []
    for i in range(len(p)):
        if not math.isnan(p[i]):
            lp.append(p[i])
            lgm5.append(gm5[i])
            lnames.append(names[i])
            lcolors.append(colors[i])
            
    pltplot(lgm5, "GM5+", lp, "P", lnames)
    
    pltplot(m2, "M2-", dv, "DV", names, colors)
    pltplot(m2, "M2-", dvov, "DV/V", names, colors)
    pltplot(m2, "M2-", desw, "DESW", names, colors)
    pltplot(m2, "M2-", de, "DE", names, colors)
    pltplot(m2, "M2-", desw_p_de, "DESW + DE", names, colors)

    lp = []
    lm2 = []
    lnames = []
    lcolors = []
    for i in range(len(p)):
        if not math.isnan(p[i]):
            lp.append(p[i])
            lm2.append(m2[i])
            lnames.append(names[i])
            lcolors.append(colors[i])
            
    pltplot(lm2, "M2-", lp, "P", lnames)

if args.show or args.cshow != "":
    matplotlib.pyplot.show()
