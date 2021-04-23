import sys
import glob
import argparse
import numpy as np
import pandas as pd

sys.path.append("./common/")

import matinfmod 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--dir", help="input csv files root dir ", \
            required=True, type=str)
    parser.add_argument("-n", help="input formulas to dump defaul=10 ", \
            required=False, type=int, default=10)
    parser.add_argument("--abc", help="extract formula having A B C ", \
            required=False, action="store_true", default=False)

    args = parser.parse_args()
    
    all_files = glob.glob(args.dir + "/*.csv_*")

    li = []

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    for filename in all_files:
        dfi = pd.read_csv(filename, index_col=None, header=0)
        dfi = dfi.sort_values('rmse')
        selectedi = dfi.head(1)
        print(selectedi[["formulas", "rmse"]])

        li.append(dfi)

    df = pd.concat(li, axis=0, ignore_index=True)

    if args.abc:
        dfa = df[df['formulas'].str.contains("_A")]
        dfb = dfa[dfa['formulas'].str.contains("_B")]
        df = dfb[dfb['formulas'].str.contains("_C")]

    df = df.sort_values('rmse')

    selected = df.head(args.n)

    previousvalue = float("inf")
    for f in selected[["formulas", "rmse"]].values:
        rmse = math.sqrt(f[1])
        if rmse != previousvalue:
           print(f[0], rmse)
           previousvalue =  rmse

