import pandas as pd
import numpy as np

#import matplotlib
#import matplotlib.pyplot as plt
#import seaborn as sns

import argparse
import math
import sys
import os

import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append("./common/")

import matinfmod 

# get from here https://stackoverflow.com/questions/17778394/list-highest-correlation-pairs-from-a-large-correlation-matrix-in-pandas
def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))

    return pairs_to_drop

def get_top_abs_correlations(df, n=5):

    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)

    return au_corr[0:n]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="input xlsx file ", \
                        required=False, default="", type=str)
    parser.add_argument("-b","--basicfeatures", \
                        help="input ; separated list of basic featuresto combine \n" + \
                        "   each feature has an associated type (i.e. \"IP[1];EA[1];Z[2]\"", \
                        required=True, type=str)
    parser.add_argument("-d", "--dumponly", \
                        help="to dump only the first N formulas",
                        required=False, type=int, default=-1)
    parser.add_argument("-v", "--verbose", \
                        help="verbose mode", action="store_true",
                        required=False, default=False)
    parser.add_argument("-l", "--labelname", \
                        help="set the label to be used default=Delta",
                        required=False, default="Delta", type=str)
    parser.add_argument("-r", "--reducemem", \
                        help="use less memory for correlation", action="store_true",
                        required=False, default=False)
    parser.add_argument("-j", "--jumpremoving", \
                        help="Do not filter the features considering the correlation", action="store_true",
                        required=False, default=False)
    parser.add_argument("-s", "--split", \
                        help="Split by a key [default=\"\"]", required=False, default="")
 
    
    args = parser.parse_args()
    
    xslxfilename = args.file

    xls = pd.ExcelFile(xslxfilename)
    data = pd.read_excel(xls, "param")

    y = data["Delta"].values
    
    atomicdata = pd.read_excel(xls, "atomicdata")
    lista = []
    listb = []
    listc = []

    for atoms in data["Name"].values:
        satoms = atoms.split(" ")
        if len(satoms) != 3:
            print("error in number of files")
            exit(1)

        lista.append(satoms[0])
        listb.append(satoms[1])
        listc.append(satoms[2])

    basicfeatureslist = args.basicfeatures.split(";")
    basicfeaturesdict = {}
    for b in basicfeatureslist:
        newb = b.split("[")
        if len(newb) != 2:
            print("Error in basicfeatures format")
            exit(1)
            
        classe = newb[1].replace("]", "")
        name = newb[0]
        
        if not (name in atomicdata.columns):
            print("Error feature not present")
            exit(1)
            
        if not (classe in basicfeaturesdict):
            basicfeaturesdict[classe] = []
            basicfeaturesdict[classe].append(name)
        else:
            basicfeaturesdict[classe].append(name)
