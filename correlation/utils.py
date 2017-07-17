import sys

import numpy 
import math
import matplotlib.pyplot 
import scipy.stats

###############################################################################

LIMITNUMOF = 5

###############################################################################

colors_map = {"A": "#66ab8c", \
        "B" : "#fff7c0", \
        "C" : "#fa7c92", \
        "D" : "#1acefc", \
        "E" : "#cb82fd", \
        "F" : "#c07eee", \
        "G" : "#ffa80b", \
        "H" : "#b6c8f5", \
        "I" : "#cca0a7", \
        "L" : "#fb7572", \
        "M" : "#f043e0", \
        "N" : "#f0f48a", \
        "O" : "#00c499", \
        "P" : "#6ec4db", \
        "R" : "#7ba462", \
        "V" : "#b56d8a"}


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

def compute_and_print_single_corr (x, y):

    pP = 0.0
    pS = 0.0 
    pK = 0.0

    if len(x) == len(y):
        if (len(y) >= LIMITNUMOF):
            pP, pS, pK = corrval(numpy.asarray(x), numpy.asarray(y))
    
    sys.stdout.write(" , %5.2f P , %5.2f S , %5.2f K \n"%(pP, pS, pK))


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

