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
  for b in basicfeatureslist:
      newb = b.split("[")
      #if len(newb) != 2:


  try:
      formula = "(IP + EA)/Z"
      newf = matinfmod.get_new_feature(atomicdata, formula)

      #print (formula)
      #for v in newf:
      #    print("%10.5f"%v)

  except NameError as err:
      print(err)

