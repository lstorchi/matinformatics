import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy

from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn import linear_model 
from sklearn.metrics import mean_absolute_error

import argparse
import math
import sys

from dataclasses import dataclass

###############################################################################

@dataclass
class atomicval:
    IP: float
    EA: float
    rs: float 
    rp: float
    rd: float

###############################################################################

def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']

###############################################################################

def replace_by_number (features, name):

  gsset = set()
  for c in features[name]:
      gsset.add(c)

  gsmap = {}
  num = 0
  for c in gsset:
      num = num + 1
      gsmap[c] = num
     
  features[name].replace(gsmap, inplace=True)

###############################################################################

def drop_all_but (features, alllist):
    for name in features.head(1):
        if not (name in alllist):
            features = features.drop(name, axis=1)


    return features

###############################################################################

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="input xlsx file ", \
          required=True, type=str)
  parser.add_argument("-a","--atomic-data-file", help="input xlsx file ", \
          required=True, type=str, dest='atomicdata')
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
  atomicfile = args.atomicdata

  atomicrawdata = pd.read_excel(atomicfile)

  atomicdata = {}

  for i in range(len(atomicrawdata["Z"].values)):
      p = atomicval(atomicrawdata["IP"].values[i], \
              atomicrawdata["EA"].values[i], \
              atomicrawdata["rs"].values[i], \
              atomicrawdata["rp"].values[i], \
              atomicrawdata["rd"].values[i])

      atomicdata[atomicrawdata["Z"].values[i]] = p

  #print(atomicrawdata["Z"].values)
  #print(atomicrawdata["EA"].values)
  #print(atomicrawdata["IP"].values)
  #print(atomicrawdata["rs"].values)
  #print(atomicrawdata["rp"].values)
  #print(atomicrawdata["rd"].values)

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

  new_features = []
  for i in range(len(val_labels)):
      new_features.append((atomicdata[features.values[i][1]].EA - \
              atomicdata[features.values[i][1]].IP) / \
              atomicdata[features.values[i][0]].rp**2)
  #plt.scatter(new_features, val_labels)
  #plt.show()


  """
  val_features = numpy.asarray(new_features)
  val_features = val_features.reshape(-1, 1)
  #print(val_features)

  reg = linear_model.LinearRegression(copy_X=True, 
          fit_intercept=True, n_jobs=None, normalize=False)
  reg.fit(val_features, val_labels)

  print(reg.coef_ , reg.intercept_)
  """

  # Compute the rbf (gaussian) kernel between X and Y
  sigma = 0.1
  clf = KernelRidge(kernel='rbf', gamma=(1.0 / sigma ** 2))
  #clf = KernelRidge(kernel='linear', gamma=3.0e-4)
  #print(val_features.shape, val_labels.shape)

  clf.fit(val_features, val_labels)

  predict = clf.predict(val_features)

  maxae = 0.0
  for i in range(len(predict)):
      if (abs(val_labels[i] - predict[i]) > maxae):
          maxae = abs(val_labels[i] - predict[i])
  #    print (val_labels[i], predict[i])

  rms = math.sqrt(mean_squared_error(val_labels, predict))
  mae = mean_absolute_error(val_labels, predict)

  print (" RMSE: ", rms)
  print ("  MAE: ", mae)
  print ("MaxAE: ", maxae)


