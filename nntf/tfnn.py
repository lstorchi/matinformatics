import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import argparse
import sys

###############################################################################

def norm(x):
      return (x - train_stats['mean']) / train_stats['std']

###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="input csv file ", \
        required=True, type=str)

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

# Remove non numeric data 
features = features.drop("Name", axis = 1)
features = features.drop("Class", axis = 1)
features = features.drop("P", axis = 1)

# remove all non needed 
# features = features.drop("GM2-", axis = 1)
# features = features.drop("ep1", axis = 1)
# features = features.drop("ep2", axis = 1)
features = features.drop("GM5+", axis = 1)
features = features.drop("M2-", axis = 1)
features = features.drop("DV/V(% AFE-FE)", axis = 1)
features = features.drop("DeltaE", axis = 1)
features = features.drop("Delta", axis = 1)
features = features.drop("eta1", axis = 1)
features = features.drop("eta2", axis = 1)
features = features.drop("eta3", axis = 1)
features = features.drop("DV/V(% FE-PA)", axis = 1)
features = features.drop("ground_state", axis = 1)
features = features.drop("DV/V(% AFE-PA)", axis = 1)

train_dataset = features.sample(frac=0.8,random_state=0)
test_dataset = features.drop(train_dataset.index)

train_stats = train_dataset.describe()
train_stats = train_stats.transpose()
print(train_stats)

sns.pairplot(train_dataset[["GM2-", "ep1", "ep2", "DE_sw"]], diag_kind="kde")
plt.show()

test_stats = test_dataset.describe()
test_stats = test_stats.transpose()
print(test_stats)

sns.pairplot(test_dataset[["GM2-", "ep1", "ep2", "DE_sw"]], diag_kind="kde")
plt.show()

train_labels = train_dataset.pop('DE_sw')
test_labels = test_dataset.pop('DE_sw')

normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)



