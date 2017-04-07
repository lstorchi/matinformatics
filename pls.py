import math
import numpy
import sys
import re

from sklearn.cross_decomposition import PLSRegression
from sklearn.cross_decomposition import PLSCanonical
from sklearn.preprocessing import scale

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

X = numpy.asarray(dataX)
Y = numpy.asarray(dataY)

sX = X
sY = Y

pls2 = PLSRegression (n_components=3, scale=False, tol=1e-06)
#pls2 = PLSCanonical(n_components=3, scale=False, tol=1e-06, algorithm="svd")

pls2.fit (sX, sY)

Y_pred = pls2.predict(X)

diff = []
for i in range(len(Y_pred)):
    diff.append(math.fabs(Y_pred[i][0]-sY[i]))
    print Y_pred[i][0], " ", Y[i], " ", math.fabs(Y_pred[i][0]-sY[i])

print numpy.mean(diff) , " ", numpy.std(diff)
