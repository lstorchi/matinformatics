import sys
import token
import parser
import tokenize
import scipy

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

from io import StringIO

def progress_bar (count, total, status=''):

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

def generate_formulas (features):

    formulas  = []

    numer = []
    for classe in features:

        dim = len(features[classe])
        for i in range(dim):
            for j in range(i+1,dim):
                numer.append(features[classe][i] + \
                        "+" + features[classe][j])
                numer.append(features[classe][i] + \
                        "-" + features[classe][j])
                numer.append(features[classe][i] + \
                        "**2 -" + features[classe][j])
                numer.append(features[classe][i] + \
                        "**2 +" + features[classe][j])
                numer.append(features[classe][i] + \
                        "**3 -" + features[classe][j])
                numer.append(features[classe][i] + \
                        "**3 +" + features[classe][j])


    deno = []
    for classe in features:

        dim = len(features[classe])
        for i in range(dim):
            deno.append("sqrt(fabs("+features[classe][i]+"))")
            deno.append("exp("+features[classe][i]+")")
            deno.append("("+features[classe][i]+"**2)")
            deno.append("("+features[classe][i]+"**3)")

    for n in numer:
        for d in deno:
            formulas.append("("+n+")/("+d+")")
            formulas.append("("+d+")/("+n+")")
            
    if len(formulas) != len(set(formulas)):
        formulas = list(set(formulas)) 

    return formulas

def generate_formulas_AB (features, atomicdata, lista, listb):

    formulas = []
    newdataframeAB = {}
    
    if lista.shape != listb.shape:
        raise NameError("Error lists shape error ")
    
    newdataframeAB["Name"] = []
    for k in atomicdata.to_dict():
        newdataframeAB[k+"_A"] = []
        newdataframeAB[k+"_B"] = []
    
    for i in range(lista.shape[0]):
        
        aelmnt = atomicdata.index[atomicdata['Z'] == \
                                  lista[i]].tolist()[0]
        belmnt = atomicdata.index[atomicdata['Z'] == \
                                  listb[i]].tolist()[0]
                                  
        newdataframeAB["Name"].append(str(aelmnt)+ \
                                      "_"+str(belmnt))
                                  
        adict = atomicdata.loc[aelmnt, :].to_dict()
        bdict = atomicdata.loc[belmnt, :].to_dict()
        
        for k in atomicdata.to_dict():
            newdataframeAB[k+"_A"].append(adict[k])
            newdataframeAB[k+"_B"].append(bdict[k])
    
    featuresAB = pd.DataFrame.from_dict(newdataframeAB) 
    
    numer = []
    
    for classe in features:
        dim = len(features[classe])
        
        f1 = []
        f2 = []
        f3 = []
        f4 = []
        f5 = []
        for i in range(dim):
            
            f1.append(features[classe][i] + "_A")
            f1.append(features[classe][i] + "_B")
            
            f2.append(features[classe][i] + "_A**2")
            f2.append(features[classe][i] + "_B**2")
            
            f3.append(features[classe][i] + "_A**3")
            f3.append(features[classe][i] + "_B**3")
            
            f4.append("sqrt(fabs("+features[classe][i] + "_A))")
            f4.append("sqrt(fabs("+features[classe][i] + "_B))")
            
            f5.append("exp("+features[classe][i] + "_A)")
            f5.append("exp("+features[classe][i] + "_B)")

        
        ftuple = (f1, f2, f3, f4, f5)
        
        for i in range(len(ftuple)):
            first = ftuple[i]
            for j in range(i, len(ftuple)):
                second = ftuple[j]
                for f in first:
                    for s in second:
                        if f != s:
                            numer.append(f + " + " + s)
                            numer.append(f + " - " + s)

    deno = []
    for classe in features:
        dim = len(features[classe])
        for i in range(dim):
            deno.append("sqrt(fabs("+features[classe][i]+"_A))")
            deno.append("exp("+features[classe][i]+"_A)")
            deno.append("("+features[classe][i]+"_A**2)")
            deno.append("("+features[classe][i]+"_A**3)")
            deno.append("sqrt(fabs("+features[classe][i]+"_B))")
            deno.append("exp("+features[classe][i]+"_B)")
            deno.append("("+features[classe][i]+"_B**2)")
            deno.append("("+features[classe][i]+"_B**3)")

    for n in numer:
        for d in deno:
            formulas.append("("+n+")/("+d+")")
            
    if len(formulas) != len(set(formulas)):
        formulas = list(set(formulas)) 

    return formulas, featuresAB


def get_new_feature (indatframe, formula):

    from math import exp, sqrt, fabs

    code = parser.expr(formula).compile()
    sio = StringIO(formula)
    tokens = tokenize.generate_tokens(sio.readline)
    
    variables = []
    for toknum, tokval, _, _, _  in tokens:
        if toknum == token.NAME:
            if (tokval != "exp") and (tokval != "sqrt") and (tokval != "fabs"):
                variables.append(tokval)
                if not (tokval in indatframe.columns):
                    raise NameError("Error ", tokval, \
                            " not in or undefined function ")

    todefinevars = ""
    for vname in variables:
        exec(vname + "_list = []")
        todefinevars += vname + " = None\n"
        for v in indatframe[vname].tolist():
            exec(vname + "_list.append("+str(v)+")")

    returnvalues = []
    # define the needed constant 
    exec(todefinevars)
    for i in range(len(indatframe[variables[0]].tolist())):
        for vname in variables:
            exec(vname + " = " + vname + "_list["+str(i)+"]")
        
        nf = eval(code)
        returnvalues.append(nf)

    return  returnvalues

def feature_check_lr(feature_list_indexes, dataset_features, y_array):

    minvalue = float("inf")
    bestformula = ""
    fd = dict()

    fd['formulas'] = []
    fd['index']    = []
    fd['rmse']     = []
    fd['percoeff'] = []
    fd['pval']     = []
    
    dataset_keys = dataset_features.keys()[feature_list_indexes]
    for jj,keys in enumerate(dataset_keys):
            X = dataset_features[keys]
            val1, val2 = scipy.stats.pearsonr(dataset_features[keys].values, y_array.values)
            
            mse = []
            for ii in range(1000):
                X_train, X_test, y_train, y_test = train_test_split(X, y_array, test_size=0.1, random_state=ii)
                regressor = LinearRegression()
                regressor.fit((np.array(X_train)).reshape(-1,1), y_train)
                y_pred = regressor.predict((np.array(X_test)).reshape(-1,1))
                mse.append(mean_squared_error(y_test,y_pred))

            avg = float(np.average(mse))
            if avg < minvalue:
                minvalue = avg
                bestformula = keys
            progress_bar(jj + 1, len(dataset_keys))
            fd['formulas'].append(keys)
            fd['index'].append(jj)
            fd['rmse'].append(avg)
            fd['percoeff'].append(val1)
            fd['pval'].append(val2)

    feature_rmse_dataframe = pd.DataFrame.from_dict(fd)
    print("")

    return feature_rmse_dataframe, minvalue, bestformula

