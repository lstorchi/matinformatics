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

    ylabel = "Delta"

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
    parser.add_argument("-y", "--yvalues", \
                        help="Y label name to be used [default=\"" + ylabel + "\"]", required=False, default="")
    parser.add_argument("-m", "--method", \
                        help="Method used to generate the features [default=1]", required=False, default=1,
                        type=int)
    parser.add_argument("--variancefilter", \
                        help="Remove all the formula with small variance [default=0.0 no filter]", required=False, default=0.0,
                        type=float

    args = parser.parse_args()
    
    xslxfilename = args.file

    xls = pd.ExcelFile(xslxfilename)
    data = pd.read_excel(xls, "MaterialData")

    y = data[ylabel].values
    
    atomicdata = pd.read_excel(xls, "AtomicData")

    lista = [x.replace(" ", "") for x in  data["A"].values]
    listb = [x.replace(" ", "") for x in  data["B"].values]
    listc = [x.replace(" ", "") for x in  data["C"].values]


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

    try:
        newdataframe = {}
        print("Start generating formulas...")
        formulas, atomicdataABC = matinfmod.generate_formulas_ABC \
            (basicfeaturesdict, atomicdata, np.asarray(lista), \
            np.asarray(listb), np.asarray(listc), args.method)
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
                newf = matinfmod.get_new_feature(atomicdataABC, formula)
            except OverflowError:
                if args.verbose:
                    print("Math error in formula (overflow)", formula)
            except ZeroDivisionError:
                if args.verbose:
                    print("Math error in formula (division by zero)", formula)

            if newf is not None:
                avg = np.mean(newf)
                std = np.std(newf)
                if (math.fabs(std/avg) < args.variancefilter):
                    print("Mean and stdev %40s %20.8f %20.8f [%10.8f]"%(formula, avg, std, std/avg), \
                        file=sys.stderr)
                else:
                    newdataframe[formula] = newf
                    if args.verbose:
                        print("Add formula: ", formula)
        
        if not args.verbose:
            print()
            
        newatomicdata = pd.DataFrame.from_dict(newdataframe)      
        print ("Produced ", newatomicdata.size , " data features")

        corrlimit = 0.99

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


