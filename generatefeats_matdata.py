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
    parser.add_argument("-f","--file", help="input xlsx file ", \
                        required=True, type=str)
    parser.add_argument("-b","--basicfeatures", \
                        help="input ; separated list of basic featuresto combine \n" + \
                        "   each feature has an associated type (i.e. \"IP[1];EA[1];Z[2]\"", \
                        required=True, type=str)
    
    args = parser.parse_args()
    
    filename = args.file
    
    xls = pd.ExcelFile(filename)
    
    data = pd.read_excel(xls)
    basicfeatureslist = args.basicfeatures.split(";")
    
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
 
    except NameError as err:
        print(err)

