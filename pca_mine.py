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

media = numpy.zeros(n, dtype='float64')
stdev = numpy.zeros(n, dtype='float64')

media = numpy.mean(pcamat, axis=1)
stdev = numpy.std(pcamat, axis=1)

for i in range(n):
    for j in range(pcamat.shape[1]):
        pcamat[i, j] -= media[i]
        pcamat[i, j] /= stdev[i]

print "Centered: " 
print pcamat
print ""

#cov_mat = numpy.cov([pcamat[0,:],pcamat[1,:]])
#print cov_mat

c = numpy.corrcoef(pcamat)
eval, evct = numpy.linalg.eig(c)

tot = 0.0
for i in range(len(eval)):
    tot += eval[i]

eig_pairs = [(numpy.abs(eval[i]), evct[:,i]) for i in range(len(eval))]
eig_pairs.sort(key=lambda x: x[0], reverse=True)

print " "
print "Eigenpair: "
for i in range(len(eval)):
    sys.stdout.write("%10.5f ["%(eig_pairs[i][0]/tot))
    for j in range(evct.shape[0]):
        sys.stdout.write("%10.5f "%((eig_pairs[i][1])[j]))
    sys.stdout.write("]\n")

projct = numpy.zeros((n, noss), dtype='float64')

for i in range(n):
    for k in range(n):
        for j in range(pcamat.shape[1]):
            projct[i, j] += eig_pairs[i][1][k]*pcamat[k, j] 

print " "
print "Projected "
for j in range(projct.shape[1]):
    for i in range(projct.shape[0]):
        sys.stdout.write("%10.5f "%(projct[i, j]))
    sys.stdout.write("\n")

#matrix_w = numpy.hstack((eig_pairs[0][1].reshape(n,1), eig_pairs[1][1].reshape(n,1)))
#transformed = matrix_w.T.dot(pcamat)
#assert transformed.shape == (n,noss), "The matrix has not the expected dimension."

#print " "
#for j in range(transformed.shape[1]):
#    for i in range(transformed.shape[0]):
#        sys.stdout.write("%10.5f "%(transformed[i, j]))
#    sys.stdout.write("\n")
