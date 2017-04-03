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

file1 = ""
file2 = ""

if len(sys.argv) == 3:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
else:
    print "usage: ", sys.argv[0] , " file1 file2 "
    exit(1)

n1 = filecount(file1)
n2 = filecount(file2)

if n1 != n2:
    print "Different dim "
    exit(1)

a1 = numpy.zeros(n1, dtype='float64')
a2 = numpy.zeros(n2, dtype='float64')

fp1 = open(file1, "r")
fp2 = open(file2, "r")

i = 0
for l in fp1:
    a1[i] = float(l)
    i += 1

i = 0
for l in fp2:
    a2[i] = float(l)
    i += 1

fp1.close()
fp2.close()

print "P-value: " , scipy.stats.pearsonr(a1, a2)

a1m = numpy.mean(a1)
a2m = numpy.mean(a2) 
a1s = numpy.std(a1)
a2s = numpy.std(a2)

pcmp = 0.0
for i in range(n1):
    pcmp += (a1[i] - a1m)*(a2[i] - a2m)

print "P computed: ", pcmp/(n1*a1s*a2s)

print scipy.stats.spearmanr(a1, a2)
print scipy.stats.kendalltau(a1, a2)
