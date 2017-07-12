import sys

import numpy 
import math
import matplotlib.pyplot 
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

###############################################################################

LIMITNUMOF = 5

###############################################################################

colors_map = {"A": "#DC143C", \
        "E" : "#FF00FF", \
        "G" : "#7D26CD", \
        "I" : "#4169E1", \
        "O" : "#00BFFF", \
        "R" : "#00C78C", \
        "V" : "#FFFF00", \
        "B" : "#EE7600"}


###############################################################################

def corrval (a1, a2, verbose = False):

  if len(a1) == 0 or len(a2) == 0:
      return 0.0, 0.0, 0.0

  if len(a1) != len(a2):
      return 0.0, 0.0, 0.0

  P = scipy.stats.pearsonr(a1, a2)[0]
  if verbose:
      print "%4.2f "%(P) + " P "

  a1m = numpy.mean(a1)
  a2m = numpy.mean(a2) 
  a1s = numpy.std(a1)
  a2s = numpy.std(a2)

  pcmp = 0.0
  for i in range(len(a1)):
      pcmp += (a1[i] - a1m)*(a2[i] - a2m)

  #print "P computed: ", pcmp/(len(a1)*a1s*a2s)

  S = scipy.stats.spearmanr(a1, a2)[0]
  K = scipy.stats.kendalltau(a1, a2)[0]

  if verbose:
      print "%4.2f "%(S)+ " S"
      print "%4.2f "%(K)+ " K"

  return P, S, K

###############################################################################

def is_number(s):
    
    try:
        float(s)
        return True
    except ValueError:
        return False

###############################################################################

def filecount (fname):
    
    i = -1
    
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
                                    
    return i + 1

###############################################################################


def compute_and_print_corr (x, dv, dvov, desw, de, deswpde, p):

    dvP, dvS, dvK = corrval(numpy.asarray(x), numpy.asarray(dv))
    dvovP, dvovS, dvovK = corrval(numpy.asarray(x), numpy.asarray(dvov))
    deswP, deswS, deswK = corrval(numpy.asarray(x), numpy.asarray(desw))
    deP, deS, deK = corrval(numpy.asarray(x), numpy.asarray(de))
    deswpdeP, deswpdeS, deswpdeK = corrval(numpy.asarray(x), numpy.asarray(deswpde))
    xn = []
    pn = []
    for i in range(len(p)):
        if not math.isnan(p[i]):
            xn.append(x[i])
            pn.append(p[i])

    if (len(pn) >= LIMITNUMOF):
        pP, pS, pK = corrval(numpy.asarray(xn), numpy.asarray(pn))
    else:
        pP = 0.0
        pS = 0.0 
        pK = 0.0

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

