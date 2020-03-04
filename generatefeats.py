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

  try:
      formula = "(IP + EA)/Z"
      newf = matinfmod.get_new_feature(atomicdata, formula)

      print (formula)
      for v in newf:
          print("%10.5f"%v)

  except NameError as err:
      print(err)

