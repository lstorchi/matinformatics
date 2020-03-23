#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression


DE_array = np.array([-0.059, -0.038, -0.033, -0.022,  0.43 ,  0.506,  0.495,  0.466,
        1.713,  1.02 ,  0.879,  2.638, -0.146, -0.133, -0.127, -0.115,
       -0.178, -0.087, -0.055, -0.005,  0.072,  0.219,  0.212,  0.15 ,
        0.668,  0.275, -0.146, -0.165, -0.166, -0.168, -0.266, -0.369,
       -0.361, -0.35 , -0.019,  0.156,  0.152,  0.203,  0.102,  0.275,
        0.259,  0.241,  0.433,  0.341,  0.271,  0.158,  0.202, -0.136,
       -0.161, -0.164, -0.169, -0.221, -0.369, -0.375, -0.381, -0.156,
       -0.044, -0.03 ,  0.037, -0.087,  0.07 ,  0.083,  0.113,  0.15 ,
        0.17 ,  0.122,  0.08 ,  0.016,  0.581, -0.112, -0.152, -0.158,
       -0.165, -0.095, -0.326, -0.35 , -0.381,  0.808,  0.45 ,  0.264,
        0.136,  0.087]).reshape(82, 1)

def feature_check(first,last, datadict):
    dataset_features = datadict
    fd = dict()
    fd['formulas'] = []
    fd['index']    = []
    fd['rmse']     = []

    for jj,keys in enumerate(dataset_features.keys()):
        if (jj>=first)&(jj<last) :
            X = dataset_features.iloc[:,jj:(jj+1)]
            y = (DE_array)
            mse = []
            for ii in range(1000):
                X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1, random_state=ii)
                regressor = LinearRegression()
                regressor.fit(X_train, y_train)
                y_pred = regressor.predict(X_test)
                mse.append(mean_squared_error(y_test,y_pred))
            fd['formulas'].append(keys)
            fd['index'].append(jj)
            fd['rmse'].append(float	(np.average(mse)))

    feature_rmse_dataframe = pd.DataFrame.from_dict(fd)
    feature_rmse_dataframe.to_csv(('{}-{}.csv').format(first,last))

