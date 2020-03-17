import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

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
    parser.add_argument("-d", "--dumponly", \
                        help="to dump only the first N formulas",
                        required=False, type=int, default=-1)
    parser.add_argument("-v", "--verbose", \
                        help="verbose mode", action="store_true",
                        required=False, default=False)
    
    args = parser.parse_args()
    
    filename = args.file
    
    xls = pd.ExcelFile(filename)
    
    atomicdata = pd.read_excel(xls, "Atomic Data")
    basicfeatureslist = args.basicfeatures.split(";")
    materialdata = pd.read_excel(xls, "Material Data")
    
    lista =  materialdata["ZA"].values
    listb =  materialdata["ZB"].values
    
    #print(atomicdata.keys())
        
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
    
    try:
        newdataframe = {}
        print("Start generating formulas...")
        formulas, atomicdataAB = matinfmod.generate_formulas_AB \
            (basicfeaturesdict, atomicdata, lista, listb)
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
        i = 0
        max = last  
        if last < 0:
            max = len(formulas)
            
        for formula in formulas[0:last]:
            if not args.verbose:
                matinfmod.progress_bar(i, max)
                i = i + 1
            newf = matinfmod.get_new_feature(atomicdataAB, formula)
            newdataframe[formula] = newf
        
        if not args.verbose:
            print()
            
        newatomicdata = pd.DataFrame.from_dict(newdataframe)      
        print ("Produced ", newatomicdata.size , " data features")

        print ("Start removing highly correlated features...")
        corr = newatomicdata.corr(method = 'pearson').abs()
        # Select upper triangle of correlation matrix
        upper = corr.where(np.triu(\
                np.ones(corr.shape), k=1).astype(np.bool))
        to_drop = [column for column in \
                   upper.columns if any(upper[column] > 0.95)]
        
        print("  Removing ", len(to_drop), " features")
        
        if args.verbose:
            for f in to_drop:
                print("    ", f)
        
        newatomicdata = newatomicdata.drop(newatomicdata[to_drop], axis=1)
        print ("Produced ", newatomicdata.size , " data features")
        
        if (args.verbose):
            corr = newatomicdata.corr(method = 'pearson').abs()
            scorr = corr.unstack()
            so = scorr.sort_values(kind="quicksort")
        
            for index, value in so.items():
                if index[0] != index[1]:
                    print (index[0], index[1], " ==> ", value)

        newatomicdata.to_pickle("newadata.pkl")
        newatomicdata.to_csv("newadata.csv")
        
        #plt.figure(figsize=(12,10))
        #cor = newatomicdata.corr()
        #sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
        #plt.show()
        
    except NameError as err:
        print(err)

