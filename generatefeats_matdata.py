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
                        required=True, type=str)
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
 
    
    args = parser.parse_args()
    
    filename = args.file
    
    xls = pd.ExcelFile(filename)
    data = pd.read_excel(xls, index_col=0)
    basicfeatureslist = args.basicfeatures.split(";")

    data = data.drop(columns=['id', "Centre_of_mass_cordinates"])

    #for V_alpha in data["V_alpha"]:
    #   print(V_alpha)
    #   print(math.exp(V_alpha))

    corrlimit = 0.95

    atleastone = False
    print("Top Absolute Correlations")
    topcorr = get_top_abs_correlations(data, 5)
    for key, value in topcorr.items():
       print("%30s %30s %10.6f"%(key[0], key[1], value))
       if (value > corrlimit):
          atleastone = True

    if atleastone:
        print("High correlationd found among basic features")
        exit(1)

    #corrmat = data.corr()
    #ax = sns.heatmap(corrmat, annot = True, vmin=-1, vmax=1, center= 0)
    #ax = sns.heatmap(corrmat, vmin=-1, vmax=1, center= 0)
    #plt.savefig("cooheatmap.png")
    #plt.show()

    basicfeaturesdict = {}
    for b in basicfeatureslist:
        newb = b.split("[")
        if len(newb) != 2:
            print("Error in basicfeatures format")
            exit(1)
            
        classe = newb[1].replace("]", "")
        name = newb[0]
        
        if not (name in data.columns):
            print("Error feature ", name, "not present")
            for bf in data.columns:
                print("   ", bf )
            exit(1)
            
        if not (classe in basicfeaturesdict):
            basicfeaturesdict[classe] = []
            basicfeaturesdict[classe].append(name)
        else:
            basicfeaturesdict[classe].append(name)
    
    try:
        print("Start generating formulas...")
        formulas = matinfmod.generate_formulas (basicfeaturesdict)
        fname  = "formulaslist.txt"
        if os.path.exists(fname):
            os.remove(fname)
        fp = open(fname, "w")
        for f in formulas:
            fp.write(f + "\n")
        fp.close()
        print("Generated ", len(formulas) ," formulas...")

        print ("Start generating features...")
        last = args.dumponly
        i = 1
        max = last  
        if last < 0:
            max = len(formulas)

        newdataframe = {}
            
        for formula in formulas[0:last]:
            if not args.verbose:
                matinfmod.progress_bar(i, max)
                i = i + 1
            #print(formula)

            try:
                newf = matinfmod.get_new_feature(data, formula)
            except OverflowError:
                print("Math error in formula (overflow)", formula)
            except ZeroDivisionError:
                print("Math error in formula (division by zero)", formula)

            newdataframe[formula] = newf
        
        if not args.verbose:
            print()
            
        newatomicdata = pd.DataFrame.from_dict(newdataframe)      
        print ("Produced ", newatomicdata.size , " data features")

 
 
    except NameError as err:
        print(err)



