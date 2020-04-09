import pandas as pd
import numpy as np

#import matplotlib
#import matplotlib.pyplot as plt
#import seaborn as sns

import argparse
import sys
import os

sys.path.append("./common/")

import matinfmod 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="input csv file containg features and sortidx values ", \
                        required=True, type=str)
    parser.add_argument("-k","--filepki", help="input pki file containg features values ", \
                        required=True, type=str)
    parser.add_argument("-n","--numofiterations", help="Number of LR iterations [default=1000]", \
                        required=False, type=int, default=1000)
    parser.add_argument("-F","--numoffeatures", help="Number of features to be used [default=100] ", \
                        required=False, type=int, default=100)
    parser.add_argument("-s","--sortidx", help="Sorting index [default=percoeff]", \
                        required=False, type=str, default="percoeff")
    parser.add_argument("-o","--output", help="output csv file ", \
                        required=False, type=str, default="2Dfeature_rmse.csv")
    parser.add_argument("-l","--labels", help="Specify labels comma separated string", \
            required=False, type=str, default=matinfmod.defaultdevalues)
 
    correlationlimit = 0.90
    
    args = parser.parse_args()

    data = pd.read_csv(args.file)

    featuresvalue = pd.read_pickle(args.filepki)

    splitted = matinfmod.defaultdevalues.split(",")

    if featuresvalue.shape[0] != len(splitted):
        print("Labels and features dimension are not compatible")
        exit(1)

    N = featuresvalue.shape[0]
    
    DE_array = np.array(np.float64(splitted)).reshape(N, 1)

    fp = open("highly_correlated_formulas.txt", "w")

    start1dN = min(args.numoffeatures, data.shape[0])
    if args.sortidx in data.columns:
        sorteddata = data.sort_values(by = args.sortidx, ascending=False)
        start1dfeatures = sorteddata.head(start1dN)

        twoDformulas = []

        print("Produce 2D formulas...")

        idx1 = 0
        for f1 in start1dfeatures["formulas"]:

            idx2 = 0
            for f2 in start1dfeatures["formulas"]:
                if idx2 > idx1:
                  if f1 != f2:
                    Xdf = featuresvalue[[f1, f2]].copy()
                    # check correlation
                    corrval = np.fabs(Xdf.corr().values[0,1])

                    if corrval < correlationlimit:
                      twoDformulas.append((f1, f2))

                    else:
                      fp.write(f1 + " and " + f2 + " are correlated " + \
                          str(corrval) + "\n") 

                idx2 += 1

            matinfmod.progress_bar(idx1 + 1, start1dN)
            idx1 += 1

        print("")
        fp.close()

        num1Df = len(start1dfeatures["formulas"])
        print("Produced ",len(twoDformulas), " 2D features ( max ", \
                (num1Df*num1Df)-num1Df, " )")

        if len(twoDformulas) > 0:

          generatedrmse = matinfmod.feature2D_check_lr(twoDformulas, 
                  featuresvalue, DE_array, args.numofiterations)
          
          if generatedrmse is None:
              print("Error in feature2D_check_lr")
              exit(1)
          
          generatedrmse.to_csv(args.output)
          
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

