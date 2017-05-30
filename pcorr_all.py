import sys
import numpy
import scipy.stats

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
    print "usage: ", sys.argv[0] , " file1 ynum "
    exit(1)

n1 = filecount(file1) - 1

a1 = numpy.zeros(n1, dtype='float64')
a2 = numpy.zeros(n1, dtype='float64')
a3 = numpy.zeros(n1, dtype='float64')

y = numpy.zeros(n1, dtype='float64')

fp1 = open(file1, "r")

fp1.readline()

i = 0
for l in fp1:
    av = l.split()
    a1[i] = (float(av[1]))
    a2[i] = (float(av[2]))
    a3[i] = (float(av[3]))
    y[i] = float(av[int(sys.argv[2])])
    #y[i] = float(av[4])+float(av[5])
    i += 1

fp1.close()

print "a1, y"
corrval(a1, y)
print "a2, y"
corrval(a2, y)
print "a3, y"
corrval(a3, y)
