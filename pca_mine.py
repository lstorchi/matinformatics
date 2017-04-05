import sys
import numpy
import matplotlib.mlab 

###############################################################################

def filecount (fname):
    
    i = -1
    
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
                                    
    return i + 1

###############################################################################

filenames = []
n = 0

if len(sys.argv) >= 4:
    n = int(sys.argv[1])
    for i in range(2, 2+n):
        filenames.append(sys.argv[i])
else:
    print "usage: ", sys.argv[0] , " N file1 file2 ... fileN "
    print "        N should be >= 2" 
    exit(1)

noss = filecount(filenames[0])

for f in filenames:
    nnew = filecount(f)
    if nnew != noss:
        print "Different dim "
        exit(1)

pcamat = numpy.zeros((n, noss), dtype='float64')

for i in range(len(filenames)):
    fp = open(filenames[i])
    j = 0
    for l in fp:
        pcamat[i, j] = float(l) 
        j += 1
    
    fp.close()

c = numpy.corrcoef(pcamat)
eval, evct = numpy.linalg.eig(c)

tot = 0.0
for i in range(len(eval)):
    tot += eval[i]

for i in range(len(eval)):
    sys.stdout.write("%10.5f ["%(eval[i]/tot))
    for j in range(evct.shape[0]):
        sys.stdout.write("%10.5f "%(evct[j, i]))
    sys.stdout.write("]\n")


