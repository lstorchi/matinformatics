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
    parser.add_argument("-n", help="sump the first N formulas removing identical R/MSE defaul=10 ", \
            required=False, type=int, default=10)
    parser.add_argument("--abc", help="extract formula having A B C ", \
            required=False, action="store_true", default=False)
    parser.add_argument("--correlation", help="extract by correlation insteda of MSE ", \
            required=False, action="store_true", default=False)

    args = parser.parse_args()
    
    filename = args.file

    df = pd.read_csv(filename)

    if args.abc:
        dfa = df[df['formulas'].str.contains("_A")]
        dfb = dfa[dfa['formulas'].str.contains("_B")]
        df = dfb[dfb['formulas'].str.contains("_C")]

    if not args.correlation:
        df = df.sort_values('rmse')
    else:
        df = df.sort_values('percoeff', ascending=False)

    selected = df.head(args.n)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    if not args.correlation:
        previousval = float("inf")
        for f in selected[["formulas", "rmse"]].values:
            if f[1]  != previousval:
                print(f[0], f[1])
                previousval = f[1]
    else:
        print(selected[["formulas", "percoeff"]])

