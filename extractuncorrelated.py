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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k","--filepki", help="input pki file containg features values ", \
            required=True, type=str)
    parser.add_argument("-c","--corrlimit", help="Specify the correlation limit " , \
            required=False, type=float, default=0.20)
 
    args = parser.parse_args()
    
    correlationlimit = args.corrlimit

    featuresvalue = pd.read_pickle(args.filepki)

    print("Total 1D features ", featuresvalue.shape[1])


    i = 1
    while True: 

        if len(featuresvalue.columns[0]) <= 0:
            print("no more formulas left")
            break

        k1 = featuresvalue.columns[0]

        print(i , " of ", len(featuresvalue.columns), flush=True)
        
        toremove = []
        for j, k2 in enumerate(featuresvalue.columns):
            if k1 != 2:
                Xdf = featuresvalue[[k1, k2]]
                corrval = np.fabs(Xdf.corr().values[0,1])
                if corrval > correlationlimit:
                    toremove.append(k2)
                    print("  Remove ", j+1, flush=True)
        
        featuresvalue = featuresvalue.drop(columns=toremove)

        i = i + 1

        if len(toremove) == 0:
            break


    featuresvalue.to_pickle("./uncorrelated.pkl")

