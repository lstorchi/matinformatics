import sys
import re

###############################################################################

def filecount (fname):
    
    i = -1
    
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
                                    
    return i + 1

###############################################################################

file = ""

if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " file "
    exit(1)

fp = open(file, "r")

dataX = []
dataY = []

dim = 0
for l in fp:
    ls = re.sub(' +',' ', l)
    splitted = ls.split()

    newdim = len(splitted)
    if dim != 0:
        if newdim != dim:
            print "File format error"
            exit(1)

    X = []
    for i in range(1, newdim-1):
        X.append(float(splitted[i]))

    dataY.append(float(splitted[newdim-1]))

    dataX.append(X)

#print dataX, dataY
