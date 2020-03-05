import pandas as pd

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
        formulas = matinfmod.generate_formulas (basicfeaturesdict)
        for formula in formulas:
            newf = matinfmod.get_new_feature(atomicdata, formula)
            
            newdataframe[formula] = newf
            print (formula)
            
        newatomicdata = pd.DataFrame.from_dict(newdataframe)
    except NameError as err:
        print(err)

