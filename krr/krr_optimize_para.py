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
  parser.add_argument("-t","--topredict", help="input property to predict ", \
          required=True, type=str)
  parser.add_argument("-r","--descriptor", help="input descriptor to use \"name1;...\" ", \
          required=True, type=str)
  parser.add_argument("-d","--dumpgraphs", help="dump graphs ", \
          required=False, default=False, action='store_true')
  
  if len(sys.argv) == 1:
      parser.print_help()
      exit(1)
  
  args = parser.parse_args()
  
  filename = args.file

  features = pd.read_excel(filename)
  print('The shape of our features is:', features.shape)
  print ("Header: ")
  i = 0
  for name in features.head(1):
      print("%5d "%(i) + name)
      i = i + 1
  
  # replace class
  replace_by_number (features, "Classification")

  fulllist = []

  if not (args.topredict in features.head(1)):
      print ("Error in topredict option")
      exit()

  fulllist.append(args.topredict)

  for desc in args.descriptor.split(";"):
       if not (desc in features.head(1)):
           print ("Error in descriptor")
           exit()

       fulllist.append(desc)

  features = drop_all_but (features, fulllist)

  if args.dumpgraphs:
      sns.pairplot(features[fulllist], 
              diag_kind="kde")
      plt.savefig('fulldataset.png')

  labels = features.pop(args.topredict)

  #print(features.values[0][0], atomicdata[features.values[0][0]])
  #print ("Features")
  #print (features)
  #print ("Labels")
  #print (labels)

  val_features = features.values
  val_labels = labels.values

  grid = (krr_param_selection (val_features, val_labels, 5))


  params = grid.best_params_
  print ("Best score: ", grid.best_score_)
  print ("Optimized params: ", params)

  clf = KernelRidge(alpha = params["alpha"], kernel='rbf', gamma= params["gamma"])
  clf.fit(val_features, val_labels)

  predict = clf.predict(val_features)

  absolutediff = [abs(x - y) for x, y in zip(val_labels, predict)]

  rms = math.sqrt(mean_squared_error(val_labels, predict))
  mae = mean_absolute_error(val_labels, predict)
  maxae = max(absolutediff)

  print (" RMSE: %E"%rms)
  print ("  MAE: %E"%mae)
  print ("MaxAE: %E"%maxae)

  #plt.clf()
  #plt.plot(absolutediff, 'bo')
  #n, bins, patches = plt.hist(absolutediff, 50, density=True, \
  #        facecolor='g', alpha=0.75)
  #plt.title('Histogram')
  #plt.grid(True)
  #plt.show()
