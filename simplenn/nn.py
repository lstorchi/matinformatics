import sys
import math
import scipy
import numpy 
import pandas
import argparse

from sklearn.model_selection import train_test_split

from snn import *

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="input csv file ", \
        required=True, type=str)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

filename = args.file

features = pandas.read_excel(filename)
print('The shape of our features is:', features.shape)
print ("Header: ")
i = 0
for name in features.head(1):
    print("%5d "%(i) + name)
    i = i + 1

print("")
print("Values basic statistics")
descriptors = features.describe()
for i in range(len(descriptors.columns)):
    print ("%5d "%(i) + descriptors.iloc[:, i].name)
    print (descriptors.iloc[:, i])


# Labels are the values we want to predict
labels = numpy.array(features["DE_sw"])

# Remove it from the features
features = features.drop("DE_sw", axis = 1)

# Remove non numeric data 
features = features.drop("Name", axis = 1)
features = features.drop("Class", axis = 1)
features = features.drop("P", axis = 1)

# remove all non needed 
# features = features.drop("GM2-", axis = 1)
features = features.drop("GM5+", axis = 1)
features = features.drop("M2-", axis = 1)
features = features.drop("DV/V(% AFE-FE)", axis = 1)
features = features.drop("DeltaE", axis = 1)
features = features.drop("Delta", axis = 1)
features = features.drop("eta1", axis = 1)
features = features.drop("eta2", axis = 1)
features = features.drop("eta3", axis = 1)
#features = features.drop("ep1", axis = 1)
#features = features.drop("ep2", axis = 1)
features = features.drop("DV/V(% FE-PA)", axis = 1)
features = features.drop("ground_state", axis = 1)
features = features.drop("DV/V(% AFE-PA)", axis = 1)

feature_list = list(features.columns)

features = numpy.array(features)

perc_of_testset = 0.10
train_features, test_features, train_labels, test_labels = \
        train_test_split(features, labels, test_size = perc_of_testset, \
        random_state = 42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

y = numpy.zeros((labels.shape[0],1), dtype=float)
y = labels.transpose()
y.shape = (labels.shape[0],1)

nn = simplenn(features, y)
for i in range(5000):
    nn.feedforward()
    nn.backprop()

nx = numpy.array(test_features)
#print("Insert ", nx)

nn.set_pred_input (nx)
nn.feedforward()
for i in range(nn.get_output().shape[0]):
    print("%10.5f %10.5f \n"%(nn.get_output()[i], test_labels[i]))
