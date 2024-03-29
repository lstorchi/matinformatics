import pandas as pd
import numpy as np

#import matplotlib
#import matplotlib.pyplot as plt
#import seaborn as sns

import argparse
import math
import sys
import os

from mendeleev import element

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
    parser.add_argument("-r", "--reducemem", \
                        help="use less memory for correlation", action="store_true",
                        required=False, default=False)
    parser.add_argument("-j", "--jumpremoving", \
                        help="Do not filter the features considering the correlation", action="store_true",
                        required=False, default=False)
    parser.add_argument("-m", "--method", \
                        help="Method used to generate the features [default=1]", required=False, default=1,
                        type=int)
    parser.add_argument("--variancefilter", \
                        help="Remove all the formula with small variance [default=0.0 no filter]", required=False, default=0.0,
                        type=float)
    
    args = parser.parse_args()
    
    filename = args.file
    
    xls = pd.ExcelFile(filename)
    basicfeatureslist = args.basicfeatures.split(";")
    data = pd.read_excel(xls)

    if (len(basicfeatureslist) <= 1):
        print("Basic features thata can be used:")
        for basicf in data.columns:
            print("  \""+basicf+"\"")
        exit(1)

    #print(atomicdata.keys())
        
    basicfeaturesdict = {}
    for b in basicfeatureslist:
        newb = b.split("[")
        if len(newb) != 2:
            print("Error in basicfeatures format")
            exit(1)
            
        classe = newb[1].replace("]", "")
        name = newb[0]
        
        if not (name in data.columns):
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
        formulas, atomicdataAB = matinfmod.generate_formulas_AB_mixed \
            (basicfeaturesdict, data, args.method)

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
            
        for formula in formulas[0:last]:
            if not args.verbose:
                matinfmod.progress_bar(i, max)
                i = i + 1

            newf = None
            try:
                newf = matinfmod.get_new_feature(atomicdataAB, formula)
            except ZeroDivisionError as zd:
                newf = None
                print("Cannot add ", formula, file=sys.stderr)
            
            if newf != None:
                avg = np.mean(newf)
                std = np.std(newf)
                if (math.fabs(std/avg) < args.variancefilter):
                    print("Mean and stdev %40s %20.8f %20.8f [%10.8f]"%(formula, avg, std, std/avg), \
                        file=sys.stderr)
                else:
                    newdataframe[formula] = newf
            
        newatomicdata = pd.DataFrame.from_dict(newdataframe)      
        print ("Produced ", newatomicdata.size , " data features")

        corrlimit = 0.90

        if not args.jumpremoving:
            print ("Start removing highly correlated features (limit: %10.5f)"%corrlimit)
            if args.reducemem:
                cname = list(newatomicdata.columns)
                
                to_drop = []
                for i in range(len(cname)):
                    if not args.verbose:
                        matinfmod.progress_bar(i+1, len(cname))
                    f1 = cname[i]
                    for j in range(i+1,len(cname)):
                        f2 = cname[j]
                        if not (f2 in to_drop):
                            corrvalue = abs(newatomicdata[f1].corr(newatomicdata[f2], \
                                                           method='pearson'))
                        
                            #print(f1, f2, corrvalue)
                            if (corrvalue > corrlimit):
                                to_drop.append(f2)
                                break
            
                if not args.verbose:
                    print("")
                print("  Removing ", len(to_drop), " features")
                
                if args.verbose:
                    for f in to_drop:
                        print("    ", f)
                
                newatomicdata = newatomicdata.drop(newatomicdata[to_drop], axis=1)
                print ("Produced ", newatomicdata.size , " data features")
            
            #    Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
            else:
                corr = newatomicdata.corr(method = 'pearson').abs()
                            
                # Select upper triangle of correlation matrix
                upper = corr.where(np.triu(\
                    np.ones(corr.shape), k=1).astype(np.bool))
                to_drop = [column for column in \
                    upper.columns if any(upper[column] > corrlimit)]
            
                print("  Removing ", len(to_drop), " features")
            
                if args.verbose:
                    for f in to_drop:
                        print("    ", f)
            
                newatomicdata = newatomicdata.drop(newatomicdata[to_drop], axis=1)
                print ("Produced ", newatomicdata.size , " data features")
        
                #if (args.verbose):
                #    corr = newatomicdata.corr(method = 'pearson').abs()
                #    scorr = corr.unstack()
                #    so = scorr.sort_values(kind="quicksort")
                
                #    for index, value in so.items():
                #        if index[0] != index[1]:
                #            print (index[0], index[1], " ==> ", value)
                
                fname = "finalformulalist.txt"
                if os.path.exists(fname):
                    os.remove(fname)
                fp = open(fname, "w")
                for f in newatomicdata:
                    fp.write(f + "\n")
                fp.close()
        
        newatomicdata.to_pickle("newadata.pkl")
        newatomicdata.to_csv("newadata.csv")
        
        #plt.figure(figsize=(12,10))
        #cor = newatomicdata.corr()
        #sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
        #plt.show()
        
    except NameError as err:
        print(err)

