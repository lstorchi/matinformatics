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

    toremove = []
    for i, k1 in enumerate(featuresvalue.columns):
        print(i+1 , " of ", len(featuresvalue.columns))
        for k2 in featuresvalue.columns:
            if k1 != 2:
                if not ((k1 in toremove) and (k2 in toremove)):
                    Xdf = featuresvalue[[k1, k2]]
                    corrval = np.fabs(Xdf.corr().values[0,1])
                    if corrval > correlationlimit:
                        toremove.append(k2)

    print(len(toremove), " To remove ", toremove )

    df = featuresvalue.drop(columns=toremove)
    df.to_pickle("./uncorrelated.pkl")



                    