import sys
import math
import numpy
import scipy.stats

###############################################################################

file1 = ""

if len(sys.argv) == 2:
    file1 = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " file1 "
    exit(1)

fp1 = open(file1, "r")

l = fp1.readline()
av = l.split()
for i in range(len(av)-1):
    sys.stdout.write("%15s , "%(av[i]))
sys.stdout.write("%15s \n"%(av[i+1]))

for i in range(len(av)-1):
    sys.stderr.write("%15s , "%(av[i]))
sys.stderr.write("%15s \n"%(av[i+1]))

i = 0
for l in fp1:
    av = l.split()
    eta1 = (float(av[1]))
    eta2 = (float(av[2]))
    eta3 = (float(av[3]))
    eta4 = (float(av[4]))
    eta5 = (float(av[5]))

    gm2 = float(av[6])
    gm5 = float(av[7])
    m2 = float(av[8])

    desw = float(av[11])
    de = float(av[12])

    sys.stderr.write("%10s ,"%(av[0]))
    for i in range(1,len(av)-1):
        sys.stderr.write("%15.10f , "%(float(av[i])))
    if av[i+1] == "metal":
        sys.stderr.write("%15s\n"%((av[i+1])))
    else:
        sys.stderr.write("%15.10f\n"%(float(av[i+1])))

    if (math.fabs(gm2) < 0.001):
        if (math.fabs(desw) > 0.001):
            print "Error " 
            exit(1)

    if (math.fabs(gm2) > 0.001):
        if (math.fabs(eta1) < 0.1) and (math.fabs(eta2) < 0.1) and \
                (math.fabs(eta3) < 0.1) and (math.fabs(eta4) < 0.1) and \
                (math.fabs(eta5) < 0.1):
          sys.stdout.write("%10s ,"%(av[0]))
          for i in range(1,len(av)-1):
              sys.stdout.write("%15.10f , "%(float(av[i])))
          if av[i+1] == "metal":
              sys.stdout.write("%15s\n"%((av[i+1])))
          else:
              sys.stdout.write("%15.10f\n"%(float(av[i+1])))
      
fp1.close()
