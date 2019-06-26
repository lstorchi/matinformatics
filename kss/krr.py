import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error

import argparse
import math
import sys

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
  parser.add_argument("-f","--file", help="input csv file ", \
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

  #print ("Features")
  #print (features)
  #print ("Labels")
  #print (labels)

  # Compute the rbf (gaussian) kernel between X and Y
  clf = KernelRidge(kernel='rbf', gamma=0.1)
  #clf = KernelRidge(kernel='linear', gamma=0.1)
  clf.fit(features.values, labels.values)

  predict = clf.predict(features.values)

  #for i in range(len(predict)):
  #    print (labels.values[i], predict[i])

  rms = math.sqrt(mean_squared_error(labels.values, predict))

  print (rms)
