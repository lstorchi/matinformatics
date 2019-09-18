import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy

from sklearn.linear_model import Lasso
import argparse
import math
import sys

from dataclasses import dataclass

from basics import *

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="input xlsx file ", \
          required=True, type=str)
  parser.add_argument("-a","--atomic-data-file", help="input xlsx file ", \
          required=True, type=str, dest='atomicdata')
  parser.add_argument("-t","--topredict", help="input property to predict ", \
          required=True, type=str)
  parser.add_argument("-d","--dumpgraphs", help="dump graphs ", \
          required=False, default=False, action='store_true')
  parser.add_argument("--features-dim", help=" use 1D , 2D or 3D desciptor / features ", \
          required=False, default=1, type=int, dest='descdim')
 
  if len(sys.argv) == 1:
      parser.print_help()
      exit(1)
  
  args = parser.parse_args()
  
  filename = args.file
  descdim = args.descdim
  atomicfile = args.atomicdata
  atomicdata = read_atomic_data(atomicfile)

  if descdim not in [1, 2, 3]:
      print ("features-dim can be 1 , 2 or 3")
      exit(1)

  alldata = pd.read_excel(filename)
  print('The shape of our alldata is:', alldata.shape)
  print ("Header: ")
  i = 0
  for name in alldata.head(1):
      print("%5d "%(i) + name)
      i = i + 1
  
  # replace class
  replace_by_number (alldata, "Classification")

  fulllist = []

  if not (args.topredict in alldata.head(1)):
      print ("Error in topredict option")
      exit()

  fulllist.append(args.topredict)

  for desc in ["ZA", "ZB"]:
       if not (desc in alldata.head(1)):
           print ("Error in data")
           exit()

       fulllist.append(desc)

  alldata = drop_all_but (alldata, fulllist)

  if args.dumpgraphs:
      sns.pairplot(alldata[fulllist], 
              diag_kind="kde")
      plt.savefig('fulldataset.png')

  labels = alldata.pop(args.topredict)

  val_labels = labels.values

  # 1d Descriptor
  new_features = []
  for i in range(len(val_labels)):
      first = (atomicdata[alldata.values[i][1]].EA - \
              atomicdata[alldata.values[i][1]].IP) / \
              (atomicdata[alldata.values[i][0]].rp**2)
      second = abs(atomicdata[alldata.values[i][0]].rs - \
              atomicdata[alldata.values[i][1]].rp) / \
              math.exp(atomicdata[alldata.values[i][0]].rs)
      third = abs(atomicdata[alldata.values[i][1]].rp - \
              atomicdata[alldata.values[i][1]].rs) / \
              math.exp(atomicdata[alldata.values[i][0]].rd)


      if descdim == 1:
          new_features.append(first)
      elif descdim == 2:
          new_features.append((first, second))
      elif descdim == 3:
          new_features.append((first, second, third))

  #plt.scatter(new_features, val_labels)
  #plt.show()

  val_features = numpy.asarray(new_features)
  if descdim == 1:
    val_features = val_features.reshape(-1, 1)

  reg = linear_model.LinearRegression(copy_X=True, 
          fit_intercept=True, n_jobs=None, normalize=False)
  reg.fit(val_features, val_labels)

  lasso = Lasso(alpha=0.01, max_iter=10e5)
  lasso.fit(val_features, val_labels)
  train_score = lasso.score(val_features, val_labels)
  coeff_used = numpy.sum(lasso.coef_!=0)
  print ("LASSO training score:", train_score )
  print ("LASSO number of features used: ", coeff_used)
  print ("LASSO coeff: ", lasso.coef_)
  

  print("Linear model: ", reg.coef_ , " ", reg.intercept_)
