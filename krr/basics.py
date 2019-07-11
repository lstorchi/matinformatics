import math

import pandas as pd

from sklearn import linear_model 
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

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

def read_atomic_data (filename):

  atomicrawdata = pd.read_excel(filename)

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

  return atomicdata


###############################################################################

def gaussian_krr (train_features, train_labels, test_features, test_labels, \
        sigma = 0.1, alphain = 1.0):

  clf = KernelRidge(alpha = alphain, kernel='rbf', gamma=(1.0 / sigma ** 2))
  #clf = KernelRidge(kernel='linear', gamma=3.0e-4)
  #print(val_features.shape, val_labels.shape)

  clf.fit(train_features, train_labels)

  predict = clf.predict(test_features)

  absolutediff = [abs(x - y) for x, y in zip(test_labels, predict)]

  rms = math.sqrt(mean_squared_error(test_labels, predict))
  mae = mean_absolute_error(test_labels, predict)
  maxae = max(absolutediff)

  return predict, rms, mae, maxae
