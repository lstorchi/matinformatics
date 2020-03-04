import pandas as pd

import argparse
import sys

sys.path.append("./common/")

import matinfmod 

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="input xlsx file ", \
          required=True, type=str)
 
  args = parser.parse_args()
  
  filename = args.file

  xls = pd.ExcelFile(filename)

  atomicdata = pd.read_excel(xls, "Atomic Data")

  matinfmod.get_new_feature(atomicdata, "(Z+IP)/exp(EA)")



