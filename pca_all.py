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

filename = ""
n = 0
SKIP = 6

if len(sys.argv) == 3:
    n = int(sys.argv[1])
    filename = (sys.argv[2])
else:
    print "usage: ", sys.argv[0] , " N file "
    print "        N should be >= 2" 
    exit(1)

noss = filecount(filename) - 1

pcamat = numpy.zeros((noss, n), dtype='float64')

fp = open(filename)
fp.readline()

i = 0
for l in fp:
    av = l.split(",")
    for j in range(n):
      pcamat[i, j] = float(av[j+SKIP]) 
    i += 1

fp.close()

results = matplotlib.mlab.PCA(pcamat)

#this will return a 2d array of the data projected into PCA space
#print results.Y 

for i, j, k in results.Y:
    sys.stdout.write("%10.5f , %10.5f , %10.5f\n"%(i, j, k))

# The weight vector for projecting a numdims point orarray into PCA space 
print "weight vector: "
print results.Wt

#this will return an array of variance percentages for each component
print "variance percentages: ", results.fracs

#print results.mu
#print results.s

#i = numpy.identity(pcamat.shape[1]) 
#coef = results.project(i)
#print coef

#print results.center(pcamat)
