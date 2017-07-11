import sys

import numpy 
import matplotlib.pyplot 
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

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


