import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import argparse
import sys

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
    
    atomicdata = pd.read_excel(xls, "Atomic Data")
    basicfeatureslist = args.basicfeatures.split(";")
    materialdata = pd.read_excel(xls, "Material Data")
    
    lista =  materialdata["ZA"].values
    listb =  materialdata["ZB"].values
    
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
        print("Generated ", len(formulas) ," formulas...")
            
        print ("Start generating features...")
        for formula in formulas:
            newf = matinfmod.get_new_feature(atomicdataAB, formula)
            
            newdataframe[formula] = newf
            
        newatomicdata = pd.DataFrame.from_dict(newdataframe)      
        print ("Produced ", newatomicdata.size , " features")

        newatomicdata.to_excel("newadata.xlsx")
        
        #plt.figure(figsize=(12,10))
        #cor = newatomicdata.corr()
        #sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
        #plt.show()
        
    except NameError as err:
        print(err)

