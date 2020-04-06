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
    parser.add_argument("-f","--file", help="input csv file containg features and values ", \
                        required=True, type=str)
    parser.add_argument("-o","--output", help="output csv file ", \
                        required=False, type=str, default="feature_rmse.csv")
    parser.add_argument("-n","--numofiterations", help="Number of LR iterations ", \
                        required=False, type=int, default=1000)
    parser.add_argument("-F","--numoffeatures", help="Number of features to be used ", \
                        required=False, type=int, default=100)
    parser.add_argument("-s","--sortidx", help="Sorting index ", \
                        required=False, type=str, default="percoeff")
 
    
    args = parser.parse_args()

    data = pd.read_csv(args.file)

    if args.sortidx in data.columns:
        #print(data)
        sorteddata = data.sort_values(by = args.sortidx, ascending=False)
        #print (sorteddata)

    else:
        print(args.sortidx, " not present ")
        exit(1)

