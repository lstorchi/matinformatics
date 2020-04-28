import pandas as pd
import numpy as np

#import matplotlib
#import matplotlib.pyplot as plt
#import seaborn as sns
from concurrent import futures

import argparse
import sys
import os

import time

sys.path.append("./common/")

import matinfmod 

###############################################################################

def checkcorr (inp):
    
    start1dfeatures = inp[0]
    idx1 = inp[1]
    f1 = inp[2]

    res = {}
    
    idx2 = 0
    for f2 in start1dfeatures["formulas"]:
        if idx2 > idx1:
            if f1 != f2:
                Xdf = featuresvalue[[f1, f2]].copy()
                # check correlation
                corrval = np.fabs(Xdf.corr().values[0,1])
                res[(f1 , f2)] = corrval
        idx2 += 1

    dim = len(start1dfeatures["formulas"])
    if idx1 == int(dim*0.10) or \
            idx1 == int(dim*0.20) or \
            idx1 == int(dim*0.30) or \
            idx1 == int(dim*0.40) or \
            idx1 == int(dim*0.50) or \
            idx1 == int(dim*0.60) or \
            idx1 == int(dim*0.70) or \
            idx1 == int(dim*0.80) or \
            idx1 == int(dim*0.90) or \
            idx1 == int(dim*0.99):
        print( "%15d of %15d"%(idx1, dim) )

    return res

###############################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="input csv file containg features and sortidx values ", \
            required=True, type=str)
    parser.add_argument("-k","--filepki", help="input pki file containg features values ", \
            required=True, type=str)
    parser.add_argument("-n","--numofiterations", help="Number of LR iterations [default=1000]", \
            required=False, type=int, default=1000)
    parser.add_argument("-F","--numoffeatures", help="Number of features to be used [default=-1] i.e. all ", \
            required=False, type=int, default=-1)
    parser.add_argument("-s","--sortidx", help="Sorting index [default=percoeff]", \
            required=False, type=str, default="percoeff")
    parser.add_argument("-o","--output", help="output csv file ", \
            required=False, type=str, default="2Dfeature_rmse.csv")
    parser.add_argument("-N","--nt", help="Specify Number of Threads or Processes to use", \
            required=False, type=int, default=2)
    parser.add_argument("-r","--range", help="Specify a range of 1D formulas to use " + \
            "default=\"0:-1\" i.e. all", required=False, type=str, default="0:-1")
    parser.add_argument("-v","--verbose", help="Dump extra files", 
            required=False, action="store_true", default=False)
    parser.add_argument("-S","--showiter", help="Show iterations instead of progress", 
            required=False, action="store_true", default=False)
 
    correlationlimit = 0.90
    
    args = parser.parse_args()

    data = pd.read_csv(args.file)
    featuresvalue = pd.read_pickle(args.filepki)

    print("Total 1D features ", featuresvalue.shape[1])

    splitted = matinfmod.defaultdevalues.split(",")

    if featuresvalue.shape[0] != len(splitted):
        print("Labels and features dimension are not compatible")
        exit(1)

    srange = args.range.split(":")

    if len(srange) != 2:
        print("error in range values")
        exit(1)

    startv = int(srange[0])
    endv = int(srange[1])

    start1dN = data.shape[0]
    if args.numoffeatures != -1:
        start1dN = min(args.numoffeatures, data.shape[0])

    if endv == -1:
        endv = start1dN

    if startv > start1dN or startv < 0:
        print("error in range start values ", startv)
        exit(1)

    if endv > start1dN or endv < 0:
        print("error in range end values ", endv)
        exit(1)

    N = featuresvalue.shape[0]

    if (data.shape[0] != featuresvalue.shape[1]):
        print("Error in selection")
        exit(1)

    print("I will consider 1D features ")
    print("    from ", startv, " to ", endv)

    DE_array = np.array(np.float64(splitted)).reshape(N, 1)

    fph = None
    fpl = None 

    if args.verbose:
        fph = open("highly_correlated_formulas.txt", "w")
        fpl = open("2D_non_correlated_formulas.txt", "w")

    if args.sortidx in data.columns:
        print("Sorting...", flush=True)
        sorteddata = data.sort_values(by = args.sortidx, ascending=False)
        start1dfeatures = sorteddata.head(start1dN)

        counter = 0
        idx1 = 0
        for f1 in start1dfeatures["formulas"]:
            idx2 = 0
            if (idx1 >= startv) and (idx1 < endv):
                for f2 in start1dfeatures["formulas"]:
                    if idx2 > idx1:
                        counter += 1
                    idx2 += 1
            idx1 += 1
        print("I will need to compare %10d pairs"%(counter), flush=True)
        twoDformulas = []

        print("Produce 2D formulas...")
        dim = len(start1dfeatures["formulas"])

        if args.nt == 1:

            avgtime = 0.0
            counter = 0
            idx1 = 0
            dim = endv - startv
            for f1 in start1dfeatures["formulas"]:
                idx2 = 0

                if (idx1 >= startv) and (idx1 < endv):
                    start = time.time()
                    counter += 1
                    for f2 in start1dfeatures["formulas"]:
                        if idx2 > idx1:
                            if f1 != f2:
                                Xdf = featuresvalue[[f1, f2]].copy()
                                # check correlation
                                corrval = np.fabs(Xdf.corr().values[0,1])
                    
                                if corrval < correlationlimit:
                                    twoDformulas.append((f1 , f2))
                    
                        idx2 += 1

                    end = time.time()

                    if args.showiter:
                        avgtime += (end - start)
                        est = (float(dim)*(avgtime/float(counter)))/3600.0
                        print("Iter %10d of %10d [%10.6f estimated tot. %10.6f hrs.]"%(counter, \
                                dim, (end - start), est),flush=True)

                    else:
                        matinfmod.progress_bar(counter, dim)


                idx1 += 1
        else:
            allformulas = {}
            listofinps = []

            print ("Preparing input")
            idx1 = 0
            for f1 in start1dfeatures["formulas"]:
                listofinps.append((start1dfeatures, idx1, f1))
                idx1 += 1
           
            print ("Running using ", args.nt, " threads/processes") 
            #with futures.ThreadPoolExecutor(max_workers=args.nt) as executor:
            with futures.ProcessPoolExecutor(max_workers=args.nt) as executor:
                results = executor.map(checkcorr, listofinps)
           
            print ("Collecting results")
            for res in list(results):
                allformulas.update(res)

            print ("Storing results ...")
            
            for k in allformulas.keys():
                corrval = allformulas[k]
            
                if corrval < correlationlimit:
                  twoDformulas.append(k)
                  if args.verbose:
                      fpl.write(k[0] + " and " + k[1] + " inserted " + \
                              str(corrval) + "\n")
                else:
                  if args.verbose:
                      fph.write(k[0] + " and " + k[1] + " are correlated " + \
                              str(corrval) + "\n") 
            
        print("")

        if args.verbose:
            fph.close()
            fpl.close()

        num1Df = len(start1dfeatures["formulas"])
        print("Produced ",len(twoDformulas), " 2D features ( max ", \
                (num1Df*num1Df)-num1Df, " )")

        if len(twoDformulas) > 0:

          generatedrmse = matinfmod.feature2D_check_lr(twoDformulas, 
                  featuresvalue, DE_array, args.nt, args.numofiterations, 
                  args.showiter)
          
          if generatedrmse is None:
              print("Error in feature2D_check_lr")
              exit(1)
          
          generatedrmse.to_csv(args.output + "_" + args.range.replace(":", "_"))
          
          minvalue_lr = np.min(generatedrmse['rmse'].values)
          bestformula_lr = \
              generatedrmse[generatedrmse['rmse'] \
              == minvalue_lr]['formulas'].values[0]
          
          print("")
          print(" Min LR value: ", minvalue_lr)
          print("   Related formula: ", bestformula_lr)
        else:
          print("No 2D formulas generated ")

    else:
        print(args.sortidx, " not present ")
        exit(1)

