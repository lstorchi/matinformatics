import sys
import math
import scipy
import numpy 
import pandas
import argparse

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

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
#features = features.drop("P", axis = 1)

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

numofdecisiontree = 1000
rf = RandomForestRegressor(n_estimators = numofdecisiontree, \
        random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels)

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)

# Calculate the absolute errors
errors = abs(predictions - test_labels)

# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(numpy.mean(errors), 2))

for i in range(len(predictions)):
    print("%10.5f %10.5f"%(predictions[i] , test_labels[i]))
