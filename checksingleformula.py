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
    parser.add_argument("--formulafile", \
            help="Specify the formula file to check default=finalselectedformulas.txt", \
            required=False, default="finalselectedformulas.txt")
    parser.add_argument("-n","--numofiterations", help="Number of LR iterations ", \
            required=False, type=int, default=1000)
    parser.add_argument("-i","--inputlabels", help="Specify label name and file comma separated string"+\
            "\n  \"filname.xlsx,labelcolumnname,sheetname\"", \
            required=True, type=str, default="")
    
    args = parser.parse_args()
    
    filename = args.file
    df = pd.read_pickle(filename)
    N = df.shape[0]

    sline = args.inputlabels.split(",")
    if len(sline) != 3:
        print("Error in --inputlabels option")
        exit(1)

    data = pd.read_excel(sline[0], sline[2])
    label = data[sline[1]]
    lbl_array = label.values

    print("I will process :", len(df.columns), " features " )
    
    fp = open(args.formulafile, "r")

    for formula in fp:
        formula = formula.replace("\n", "")

        if  formula in list(df.columns):
            feature_mse_dataframe = \
                   matinfmod.feature_check_lr ([list(df.columns).index(formula)], df, \
                   lbl_array, args.numofiterations)

            print(formula)
   
            minvalue_lr = np.min(feature_mse_dataframe['mse'].values)
            bestformula_lr = \
                       feature_mse_dataframe[feature_mse_dataframe['mse'] \
                       == minvalue_lr]['formulas'].values[0]
            print("LR value: ", minvalue_lr)
            pearson_max = np.max(feature_mse_dataframe['percoeff'].values)
            bestformula_pearson = \
                feature_mse_dataframe[feature_mse_dataframe['percoeff'] \
                == pearson_max]['formulas'].values[0]
            print("Pearson R value: ", pearson_max)
            pval_min = np.min(feature_mse_dataframe['pval'].values)
            bestformula_pval = \
                 feature_mse_dataframe[feature_mse_dataframe['pval'] \
                  == pval_min]['formulas'].values[0]
            print("P-Value value: ", pval_min)
            mape_min = np.min(feature_mse_dataframe['mape'].values)
            bestformula_pval = \
               feature_mse_dataframe[feature_mse_dataframe['mape'] \
               == mape_min]['formulas'].values[0]
            print("MAPE value: ", mape_min)
        else:
            print(args.formula, " not present ")

    fp.close()
     
