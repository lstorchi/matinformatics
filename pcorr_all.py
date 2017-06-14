import sys
import numpy
import scipy.stats
import pandas 

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

def corrval (a1, a2):

  print "%4.2f "%(scipy.stats.pearsonr(a1, a2)[0]) + " P "

  a1m = numpy.mean(a1)
  a2m = numpy.mean(a2) 
  a1s = numpy.std(a1)
  a2s = numpy.std(a2)

  pcmp = 0.0
  for i in range(n1):
      pcmp += (a1[i] - a1m)*(a2[i] - a2m)

  #print "P computed: ", pcmp/(n1*a1s*a2s)

  print "%4.2f "%(scipy.stats.spearmanr(a1, a2)[0])+ " S"
  print "%4.2f "%(scipy.stats.kendalltau(a1, a2)[0])+ " K"

###############################################################################

file1 = ""

if len(sys.argv) == 3:
    file1 = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " file ynum"
    exit(1)


n1 = filecount(file1) - 1

lgm2 = []
lgm5 = []
lm2 = []
ly = []

fp1 = open(file1, "r")

fp1.readline()

for l in fp1:
    av = l.split(",")

    if (is_number(av[int(sys.argv[2])])):
      yv = float(av[int(sys.argv[2])])
      lgm2.append(float(av[6]))
      lgm5.append(float(av[7]))
      lm2.append(float(av[8]))
      ly.append(yv)
      #y[i] = float(av[11])+float(av[12])

gm2 = numpy.asarray(lgm2)
gm5 = numpy.asarray(lgm5)
m2 = numpy.asarray(lm2)
y = numpy.asarray(ly)

fp1.close()

print "GM2-, y"
corrval(gm2, y)
print "GM5+, y"
corrval(gm5, y)
print "M2-, y"
corrval(m2, y)
