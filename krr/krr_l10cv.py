import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy

import argparse
import math
import sys

from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from basics import *

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="input xlsx file ", \
          required=True, type=str)
  parser.add_argument("-a","--atomic-data-file", help="input xlsx file ", \
          required=True, type=str, dest='atomicdata')
  
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
  
  topredict = "DE"
  fulllist = [topredict, "ZA", "ZB"]

  alldata = drop_all_but (alldata, fulllist)

  # 1d Descriptor
  desc_1d = []
  for i in range(len(alldata.values)):
      desc_1d.append((atomicdata[alldata.values[i][1]].EA - \
              atomicdata[alldata.values[i][1]].IP) / \
              atomicdata[alldata.values[i][0]].rp**2)

  new_features = numpy.asarray(desc_1d)
 
  features = alldata.values
  gamma = 0.1
  alpha = 0.1
  
  features = new_features
  features = features.reshape(-1, 1)
  gamma = 0.001
  alpha = 0.01

  labels = alldata.pop(topredict).values

  num_of_run = 150
  predict = []
  truevalue = []

  mean_rms = 0.0
  mean_mae = 0.0
  mean_maxae = 0.0

  for i in range(num_of_run):
      
      perc_of_testset = 0.10
      train_features, test_features, train_labels, test_labels = \
              train_test_split(features, labels, test_size = perc_of_testset, \
              random_state = i)

      #print ('Training set features')
      #print (train_features)
      #print ('\nTest set features')
      #print (test_features)

      #print ('Training set labels')
      #print (train_labels)
      #print ('\nTest set labels')
      #print (test_labels)

      #test_labels = 10.0 * numpy.random.rand(len(test_labels))

      act_predict, rms, mae, maxae = gaussian_krr (train_features, train_labels, \
              test_features, test_labels, gamma, alpha )
      
      predict.extend(act_predict)
      truevalue.extend(test_labels)

      mean_rms += rms
      mean_mae += mae
      mean_maxae += maxae

      #print (" RMSE: ", rms)
      #print ("  MAE: ", mae)
      #print ("MaxAE: ", maxae)



rms = math.sqrt(mean_squared_error(truevalue, predict))
mae = mean_absolute_error(truevalue, predict)
absdiff = [abs(x - y) for x, y in zip(truevalue, predict)]
maxae = numpy.amax(absdiff)

print (" RMSE: ", rms)
print ("  MAE: ", mae)
print ("MaxAE: ", maxae)

print ("Mean  RMSE: ", mean_rms/float(num_of_run))
print ("Mean   MAE: ", mean_mae/float(num_of_run))
print ("Mean MaxAE: ", mean_maxae/float(num_of_run))



plt.plot(absdiff, 'bo')
#n, bins, patches = plt.hist([abs(x - y) for x, y in zip(truevalue, predict)], \
#        50, density=True, \
#        facecolor='g', alpha=0.75)
#plt.title('Histogram')
plt.grid(True)
plt.show()
 
