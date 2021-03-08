import sys
import argparse
import numpy as np
import pandas as pd

sys.path.append("./common/")

import matinfmod 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="input pki file ", \
            required=True, type=str)
    parser.add_argument("-o","--output", help="output csv file [default=feature_rmse.csv]", \
            required=False, type=str, default="feature_rmse.csv")
    parser.add_argument("-n","--numofiterations", help="Number of LR iterations ", \
            required=False, type=int, default=1000)
    parser.add_argument("-i","--inputlabels", help="Specify label name and file comma separated string"+\
            "\n  \"filname.csv,labelcolumnname\"", \
            required=False, type=str, default="")
    parser.add_argument("-s", "--split", \
            help="Split by a key [default=\"\"]", required=False, default="")
    
    args = parser.parse_args()
    
    filename = args.file

    df = pd.read_pickle(filename)
    N = df.shape[0]

    DE_Array = None
    print(args.inputlabels)
    if args.inputlabels == "":
        splitted = matinfmod.defaultdevalues.split(",")
        DE_array = np.array(np.float64(splitted)).reshape(N, 1)

        if df.shape[0] != len(splitted):
                print("Labels and features dimension are not compatible")
                exit(1)
    else:
        sline = args.inputlabels.split(",")
        if len(sline) != 2:
            print("Error in --inputlabels option")
            exit(1)
        data = pd.read_csv(sline[0])

        if args.split != "":
            ssplit = args.split.split(";")
            if (len(ssplit) != 2):
                print("Error in split option ", args.split, " must have key;value pair")
                exit(1)
 
            key = ssplit[0]
            value = ssplit[1]
 
            if not (key in data.columns):
                print("Error in split option ", key, " not present ")
                exit(1)
 
            uniqvalues  = set(data[key].values)
 
            if not int(value) in uniqvalues:
                print("Error value ", int(value), " not present")
                exit(1)
 
            print("All possible value are:")
            for v in uniqvalues:
                print("  ",v)
 
            isthevalue =  data[key] == int(value)
            data = data[isthevalue]

            print("Selected data: ")
            print(data.shape)
 
        label = data[sline[1]]
        DE_array = label.values

    print("I will process :", len(df.columns), " features " )

    feature_rmse_dataframe = \
            matinfmod.feature_check_lr (range(0, len(df.columns)), df, \
            DE_array, args.numofiterations)

    feature_rmse_dataframe.to_csv(args.output)

    minvalue_lr = np.min(feature_rmse_dataframe['rmse'].values)
    bestformula_lr = \
            feature_rmse_dataframe[feature_rmse_dataframe['rmse'] \
            == minvalue_lr]['formulas'].values[0]

    print(" Min LR value: ", minvalue_lr)
    print("   Related formula: ", bestformula_lr)

    pearson_max = np.max(feature_rmse_dataframe['percoeff'].values)
    bestformula_pearson = \
            feature_rmse_dataframe[feature_rmse_dataframe['percoeff'] \
            == pearson_max]['formulas'].values[0]

    print("")
    print(" Max Pearson R value: ", pearson_max)
    print("   Related formula: ", bestformula_pearson)

    pval_min = np.min(feature_rmse_dataframe['pval'].values)
    bestformula_pval = \
            feature_rmse_dataframe[feature_rmse_dataframe['pval'] \
            == pval_min]['formulas'].values[0]

    print("")
    print(" Min P-Value value: ", pval_min)
    print("   Related formula: ", bestformula_pval)
