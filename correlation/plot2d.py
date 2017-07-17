import sys

import math 
import numpy 
import argparse

import scipy.stats
import matplotlib.pyplot 

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
parser.add_argument("-p","--showscatterplot", help="Show scatter plot for rows n and m \"n,m\" "\
        "start numbering from 0", required=True, default="", type=str)
parser.add_argument("-c","--cshow", help="display all scatter plots for a "\
        "specific class", \
        required=False, default="", type=str)

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

if len(columnum) != 2:
    print "Error two colum required"
    exit(1)

xnum = int(columnum[0])
ynum = int(columnum[1])

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

xall = []
yall = []
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

    if len (lv) < 4:
        print "Error at line ", linenum 
        exit(1) 

    if (xnum >= len (lv)) or (ynum >= len (lv)):
        print "Error at line ", linenum
        exit(1)

    linenum += 1
   
    if (lv[1] != "X"):
        if utils.is_number(lv[xnum]) and utils.is_number(lv[ynum]):
            yall.append(float(lv[ynum]))
            xall.append(float(lv[xnum]))
            names.append(lv[0]+ " ("+lv[1]+")")
            classes.append(lv[1])
            setofclasses.add(lv[1])

            if not (lv[1] in utils.colors_map.keys()):
                print "Error at line ", linenum, \
                    " color not defined for the give key ", lv[1]
                exit(1)

            colors.append(utils.colors_map[lv[1]])


fp.close()

print "Using ", len(names) , " values"

sys.stdout.write ("Correlation " + xname + " vs " + yname+  " ")
utils.compute_and_print_single_corr (xall, yall)

pltplot (xall, xname, yall, yname, names, colors)

for c in setofclasses:
    print "Selected class ", c

    s_xall = []
    s_yall = []

    s_names = []
    s_classes = []
    s_colors = []

    for i in range(len(classes)):
        if (classes[i] == c):
            s_xall.append(xall[i])
            s_yall.append(yall[i])

            s_names.append(names[i])
            s_classes.append(classes[i])
            s_colors.append(colors[i])

    if (len(s_names) >= utils.LIMITNUMOF):
        sys.stdout.write("class dim %d ,"%(len(s_names) ))
        for n in s_names:
            sys.stdout.write("%s "%(n))
        sys.stdout.write("\n")
        
        sys.stdout.write ("Correlation " + xname + " vs " + yname+  " ")
        utils.compute_and_print_single_corr (s_xall, s_yall)
    
    if (args.cshow == c):
        pltplot (s_xall, xname, s_yall, yname, s_names, s_colors)



if args.cshow != "" or args.showscatterplot != "":
    matplotlib.pyplot.show()
