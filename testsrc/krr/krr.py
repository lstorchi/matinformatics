import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy

import argparse
import math
import sys

from dataclasses import dataclass

from basics import *

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

  predict, rms, mae, maxae = gaussian_krr (val_features, val_labels, \
          val_features, val_labels, gammain = (1.0 / (0.1**2)), \
          alphain = 3.0e-4)

  print (" RMSE: %E"%rms)
  print ("  MAE: %E"%mae)
  print ("MaxAE: %E"%maxae)

  absdiff = [abs(x - y) for x, y in zip(val_labels, predict)]

  plt.clf()
  plt.plot(absdiff, 'bo')
  #n, bins, patches = plt.hist(absolutediff, 50, density=True, \
  #        facecolor='g', alpha=0.75)
  #plt.title('Histogram')
  plt.grid(True)
  plt.show()
