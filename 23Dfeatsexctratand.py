import pandas as pd
import numpy as np

#import matplotlib
#import matplotlib.pyplot as plt
#import seaborn as sns
from concurrent import futures

import argparse
import sys
import os
import re

import time

sys.path.append("./common/")

import matinfmod 

###############################################################################

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-n","--numofiterations", help="Number of LR iterations [default=1000]", \
            required=False, type=int, default=1000)
    parser.add_argument("-e","--filenames", help="Enter filenames [default=out_*]", \
            required=False, type=str, default="out_*")
    parser.add_argument("-d","--rootdir", help="Enter root dir [default=./]", \
            required=False, type=str, default="./")
    parser.add_argument("-k","--filepki", help="input pki file containg features values ", \
            required=True, type=str)
    parser.add_argument("--set3Don", help="£D features on ", \
            required=False, action="store_true", default=False)
 
 
    args = parser.parse_args()

    features = []

    print("Reading all data")

    if args.set3Don :
       for filename in os.listdir(args.rootdir):
           if re.match(args.filenames, filename):
               with open(os.path.join(args.rootdir, filename), 'r') as f:
                   for line in f:
                       if line.find("Min LR") >= 0:
                           if line.find("] [") >= 0:
                               sline = line.split("] [")
                               f1 = sline[0].replace("[", "")
                               f2 = sline[1].replace("[", "")
                               f3 = sline[2].replace("]", "").split("Min LR", 1)[0]
       
                               features.append((f1.lstrip().rstrip(), f2.lstrip().rstrip(), \
                                       f3.lstrip().rstrip()))

    else:
       for filename in os.listdir(args.rootdir):
           if re.match(args.filenames, filename):
               with open(os.path.join(args.rootdir, filename), 'r') as f:
                   for line in f:
                       if line.find("Min LR") >= 0:
                           if line.find(") (") >= 0:
                               sline = line.split(") (")
       
                               f1 = sline[0]+")"
                               f2 = "("+sline[1].split("Min LR", 1)[0]
       
                               features.append((f1.lstrip().rstrip(), f2.lstrip().rstrip()))
                           elif line.find("] [") >= 0:
                               sline = line.split("] [")
                               f1 = sline[0].replace("[", "")
                               f2 = sline[1].replace("]", "").split("Min LR", 1)[0]
       
                               features.append((f1.lstrip().rstrip(), f2.lstrip().rstrip()))


    featuresvalue = pd.read_pickle(args.filepki)

    N = featuresvalue.shape[0]
    splitted = matinfmod.defaultdevalues.split(",")
    DE_array = np.array(np.float64(splitted)).reshape(N, 1)

    print("Start LR...")

    if args.set3Don :
        generatedrmse = matinfmod.feature3D_check_lr(features, 
                  featuresvalue, DE_array, args.numofiterations, 
                  True)
    else:
        generatedrmse = matinfmod.feature2D_check_lr(features, 
                  featuresvalue, DE_array, 1, args.numofiterations, 
                  True)
 

    minvalue_lr = np.min(generatedrmse['rmse'].values)
    bestformula_lr = generatedrmse[generatedrmse['rmse'] \
                  == minvalue_lr]['formulas'].values[0]
          
    print("")

    if args.set3Don :
        print("[" + bestformula_lr[0] + "] [" + bestformula_lr[1] + \
            "] [" + bestformula_lr[2] + "] Min LR value %12.9f"%(minvalue_lr))
    else:
        print("[" + bestformula_lr[0] + "] [" + bestformula_lr[1] + \
            "] Min LR value %12.9f"%(minvalue_lr))
 
