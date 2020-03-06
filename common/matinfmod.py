import token
import parser
import tokenize

from io import StringIO

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
