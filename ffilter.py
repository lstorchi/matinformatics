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
    parser.add_argument("-o","--output", help="output csv file ", \
                        required=False, type=str, default="feature_rmse.csv")
    
    args = parser.parse_args()
    
    filename = args.file

    df = pd.read_pickle(filename)
    
    DE_array = np.array([-0.059, -0.038, -0.033, -0.022,  0.43 ,  0.506,  0.495,  0.466,
        1.713,  1.02 ,  0.879,  2.638, -0.146, -0.133, -0.127, -0.115,
       -0.178, -0.087, -0.055, -0.005,  0.072,  0.219,  0.212,  0.15 ,
        0.668,  0.275, -0.146, -0.165, -0.166, -0.168, -0.266, -0.369,
       -0.361, -0.35 , -0.019,  0.156,  0.152,  0.203,  0.102,  0.275,
        0.259,  0.241,  0.433,  0.341,  0.271,  0.158,  0.202, -0.136,
       -0.161, -0.164, -0.169, -0.221, -0.369, -0.375, -0.381, -0.156,
       -0.044, -0.03 ,  0.037, -0.087,  0.07 ,  0.083,  0.113,  0.15 ,
        0.17 ,  0.122,  0.08 ,  0.016,  0.581, -0.112, -0.152, -0.158,
       -0.165, -0.095, -0.326, -0.35 , -0.381,  0.808,  0.45 ,  0.264,
        0.136,  0.087]).reshape(82, 1)

    feature_rmse_dataframe, minvalue, bestformula = \
            matinfmod.feature_check_lr (0, len(df.columns), df, DE_array)

    print("LR resulrs: ")
    print(" Best formula: ", bestformula)
    print(" Min value: ", minvalue)

    feature_rmse_dataframe.to_csv(args.output)
