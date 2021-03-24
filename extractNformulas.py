import sys
import argparse
import numpy as np
import pandas as pd

sys.path.append("./common/")

import matinfmod 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="input csv file ", \
            required=True, type=str)
    parser.add_argument("-n", help="input formulas to dump defaul=10 ", \
            required=False, type=int, default=10)
 
    
    args = parser.parse_args()
    
    filename = args.file

    df = pd.read_csv(filename)

    df = df.sort_values('mse')

    selected = df.head(args.n)


    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    print(selected["formulas"])
