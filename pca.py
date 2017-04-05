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

pcamat = numpy.zeros((noss, n), dtype='float64')

for j in range(len(filenames)):
    fp = open(filenames[j])
    i = 0
    for l in fp:
        pcamat[i, j] = float(l) 
        i += 1
    
    fp.close()

results = matplotlib.mlab.PCA(pcamat)

#this will return an array of variance percentages for each component
#print results.fracs

#this will return a 2d array of the data projected into PCA space
#print results.Y 

for i, j in results.Y:
    sys.stdout.write("%10.5f %10.5f\n"%(i, j))

#print results.Wt
