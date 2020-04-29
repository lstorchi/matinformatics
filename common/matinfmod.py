import sys
import token
import parser
import tokenize
import scipy
import time 

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

from concurrent import futures

defaultdevalues = "-0.059, -0.038, -0.033, -0.022,  0.43 ,  0.506,  0.495,  0.466," +\
      " 1.713,  1.02 ,  0.879,  2.638, -0.146, -0.133, -0.127, -0.115," +\
      "-0.178, -0.087, -0.055, -0.005,  0.072,  0.219,  0.212,  0.15 ," +\
      " 0.668,  0.275, -0.146, -0.165, -0.166, -0.168, -0.266, -0.369," +\
      "-0.361, -0.35 , -0.019,  0.156,  0.152,  0.203,  0.102,  0.275," +\
      " 0.259,  0.241,  0.433,  0.341,  0.271,  0.158,  0.202, -0.136," +\
      "-0.161, -0.164, -0.169, -0.221, -0.369, -0.375, -0.381, -0.156," +\
      "-0.044, -0.03 ,  0.037, -0.087,  0.07 ,  0.083,  0.113,  0.15 ," +\
      " 0.17 ,  0.122,  0.08 ,  0.016,  0.581, -0.112, -0.152, -0.158," +\
      "-0.165, -0.095, -0.326, -0.35 , -0.381,  0.808,  0.45 ,  0.264," +\
      " 0.136,  0.087"


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

def feature_check_lr(feature_list_indexes, dataset_features, y_array, \
        numoflr = 1000):

    fd = dict()

    fd['formulas'] = []
    fd['index']    = []
    fd['rmse']     = []
    fd['percoeff'] = []
    fd['pval']     = []
    
    dataset_keys = dataset_features.keys()[feature_list_indexes]
    for jj,keyv in enumerate(dataset_keys):
        X = dataset_features[keyv]

        val1, val2 = \
                scipy.stats.pearsonr(dataset_features[keyv].values, \
                y_array.reshape(dataset_features[keyv].values.shape[0]))
        
        mse = []
        for ii in range(numoflr):
            X_train, X_test, y_train, y_test = \
                    train_test_split(X, y_array, test_size=0.1, random_state=ii)
            regressor = LinearRegression()
            regressor.fit((np.array(X_train)).reshape(-1,1), y_train)
            y_pred = regressor.predict((np.array(X_test)).reshape(-1,1))
            mse.append(mean_squared_error(y_test,y_pred))

        avg = float(np.average(mse))

        progress_bar(jj + 1, len(dataset_keys))
        fd['formulas'].append(keyv)
        fd['index'].append(jj)
        fd['rmse'].append(avg)
        fd['percoeff'].append(np.fabs(val1))
        fd['pval'].append(val2)

    feature_rmse_dataframe = pd.DataFrame.from_dict(fd)
    fd2 = feature_rmse_dataframe.copy()
    
    print("")
    
    return feature_rmse_dataframe


def task_feature2D_check_lr (inps):

    f1 = inps[0]
    f2 = inps[1]
    dataset_features = inps[2]
    numoflr = inps[3]
    y_array = inps[4]
    toprint = inps[5]

    avg = float("inf")
    if f1 in dataset_features.columns and \
            f2 in dataset_features.columns:
        Xdf = dataset_features[[f1, f2]].copy()
        X = Xdf.values
    
        mse = []
        for ii in range(numoflr):
            X_train, X_test, y_train, y_test = \
                    train_test_split(X, y_array, test_size=0.1, random_state=ii)
            regressor = LinearRegression()
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(X_test)
            mse.append(mean_squared_error(y_test,y_pred))
    
        avg = float(np.average(mse))

    if toprint != "":
        print(toprint)

    return (f1, f2, avg)

def feature2D_check_lr(twoDformulas, dataset_features, y_array, nt, \
        numoflr = 1000, showiter=False):

    fd = dict()

    fd['formulas'] = []
    fd['rmse']     = []

    if nt == 1:

        idx = 0
        dim = len(twoDformulas)
        avgtime = 0.0
        for f1, f2 in twoDformulas:
            start = time.time()

            Xdf = dataset_features[[f1, f2]].copy()
            X = Xdf.values
        
            mse = []
            for ii in range(numoflr):
                X_train, X_test, y_train, y_test = \
                        train_test_split(X, y_array, test_size=0.1, random_state=ii)
                regressor = LinearRegression()
                regressor.fit(X_train, y_train)
                y_pred = regressor.predict(X_test)
                mse.append(mean_squared_error(y_test,y_pred))
        
            avg = float(np.average(mse))

            fd['formulas'].append((f1, f2))
            fd['rmse'].append(avg)

            end = time.time()

            idx += 1
            if showiter:
                avgtime += (end - start)
                est = (float(dim)*(avgtime/float(idx)))/3600.0
                print("Iter %10d of %10d [%10.6f estimated tot. %10.6f hrs.]"%(idx, dim, \
                        (end - start), est),flush=True)
            else:
                progress_bar(idx, dim)
    else:

        print("Preparing input for ", nt, " threads/processes")
        inputs = []
        toprint = ""
        idx = 0
        dim = len(twoDformulas)
        for f1, f2 in twoDformulas:
            inputs.append((f1, f2, dataset_features,
                    numoflr, y_array, toprint))
            idx += 1
            if idx == int(dim*0.10) or \
                idx == int(dim*0.20) or \
                idx == int(dim*0.30) or \
                idx == int(dim*0.40) or \
                idx == int(dim*0.50) or \
                idx == int(dim*0.60) or \
                idx == int(dim*0.70) or \
                idx == int(dim*0.80) or \
                idx == int(dim*0.90) or \
                idx == int(dim*0.99):
                    toprint = "%15d of %15d"%(idx, dim) 
            else:
                toprint = ""
        
        #with futures.ThreadPoolExecutor(max_workers=nt) as executor:
        with futures.ProcessPoolExecutor(max_workers=nt) as executor:
            results = executor.map(task_feature2D_check_lr, inputs)
        
        for res in list(results):
            fd['formulas'].append((res[0], res[1]))
            fd['rmse'].append(res[2])

    return pd.DataFrame.from_dict(fd)
