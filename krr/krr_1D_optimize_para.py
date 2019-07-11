import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy

import argparse
import math
import sys

from dataclasses import dataclass

from sklearn.model_selection import GridSearchCV

from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from basics import *

###################################################################

def krr_param_selection(x, y, nfolds):
    alphas = [0.00001, 0.001, 0.01, 0.1, 1, 10]
    gammas = [0.00001, 0.001, 0.01, 0.1, 1, 10]

    alphas = [1e0, 0.1, 1e-2, 1e-3, 3.0e-4, 1e-4]
    gammas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
 
    param_grid = {'alpha': alphas, 'gamma' : gammas}
    grid_search = GridSearchCV(KernelRidge(kernel='rbf'), \
            param_grid, n_jobs = 5, cv=nfolds)
    grid_search.fit(x, y)
                                
    return grid_search

##################################################################

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
  
  if len(sys.argv) == 1:
      parser.print_help()
      exit(1)
  
  args = parser.parse_args()
  
  filename = args.file
  atomicfile = args.atomicdata

  atomicdata = read_atomic_data(atomicfile)

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
      new_features.append((atomicdata[alldata.values[i][1]].EA - \
              atomicdata[alldata.values[i][1]].IP) / \
              atomicdata[alldata.values[i][0]].rp**2)

  #plt.scatter(new_features, val_labels)
  #plt.show()

  val_features = numpy.asarray(new_features)
  val_features = val_features.reshape(-1, 1)

  reg = linear_model.LinearRegression(copy_X=True, 
          fit_intercept=True, n_jobs=None, normalize=False)
  reg.fit(val_features, val_labels)

  print("Linear model: ", reg.coef_ , " ", reg.intercept_)

  grid = krr_param_selection (val_features, val_labels, 5)

  params = grid.best_params_
  print ("Best score: ", grid.best_score_)
  print ("Optimized params: ", params)

  predict, rms, mae, maxae = gaussian_krr (val_features, val_labels, val_features, val_labels, \
        gammain = params["gamma"], alphain = params["alpha"])

  print (" RMSE: ", rms)
  print ("  MAE: ", mae)
  print ("MaxAE: ", maxae)

  absdiff = [abs(x - y) for x, y in zip(val_labels, predict)]

  plt.plot(absdiff, 'bo')
  #n, bins, patches = plt.hist([abs(x - y) for x, y in zip(truevalue, predict)], \
  #        50, density=True, \
  #        facecolor='g', alpha=0.75)
  #plt.title('Histogram')
  plt.grid(True)
  plt.show()
 
