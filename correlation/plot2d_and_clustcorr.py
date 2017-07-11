import sys

import math 
import numpy 
import matplotlib.pyplot 
import scipy.stats
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

print "Correlation GM5+"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
compute_and_print_corr (gm5, dv, dvov, desw, de, desw_p_de, p)

print "Correlation M2-"
print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
compute_and_print_corr (m2, dv, dvov, desw, de, desw_p_de, p)

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

    if (len(s_names) >= 5):
        sys.stdout.write("class dim %d ,"%(len(s_names) ))
        for n in s_names:
            sys.stdout.write("%s "%(n))
        sys.stdout.write("\n")

        print "Correlation GM2-"
        print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
        compute_and_print_corr (s_gm2, s_dv, s_dvov, s_desw, s_de, s_desw_p_de, s_p)
        
        print "Correlation GM5+"
        print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
        compute_and_print_corr (s_gm5, s_dv, s_dvov, s_desw, s_de, s_desw_p_de, s_p)
        
        print "Correlation M2-"
        print "       DV,      DV/V,    DESW,      DE,    DESW+DE,         P" 
        compute_and_print_corr (s_m2, s_dv, s_dvov, s_desw, s_de, s_desw_p_de, s_p)
 

exit(1)

pltplot(gm2, "GM2-", dv, "DV", names , "GM2- vs DV")
pltplot(gm2, "GM2-", dvov, "DV/V", names, "GM2- vs DV/V")
pltplot(gm2, "GM2-", desw, "DESW", names, "GM2- vs DESW")
pltplot(gm2, "GM2-", de, "DE", names, "GM2- vs DE")
pltplot(gm2, "GM2-", desw_p_de, "DESW + DE", names, "GM2- vs DDESW + DE")

pltplot(gm5, "GM5+", dv, "DV", names, "GM5+ vs DV")
pltplot(gm5, "GM5+", dvov, "DV/V", names, "GM5+ vs DV/V")
pltplot(gm5, "GM5+", desw, "DESW", names, "GM5+ vs DESW")
pltplot(gm5, "GM5+", de, "DE", names, "GM5+ vs DE")
pltplot(gm5, "GM5+", desw_p_de, "DESW + DE", names, "GM5+ vs DDESW + DE")

pltplot(m2, "M2-", dv, "DV", names, "M2- vs DV")
pltplot(m2, "M2-", dvov, "DV/V", names, "M2- vs DV/V")
pltplot(m2, "M2-", desw, "DESW", names, "M2- vs DESW")
pltplot(m2, "M2-", de, "DE", names, "M2- vs DE")
pltplot(m2, "M2-", desw_p_de, "DESW + DE", names, "M2- vs DDESW + DE")

matplotlib.pyplot.show()
