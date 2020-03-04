import token
import parser
import tokenize

from io import StringIO

def get_new_feature (indatframe, formula):

    from math import exp, sqrt

    code = parser.expr(formula).compile()
    sio = StringIO(formula)
    tokens = tokenize.generate_tokens(sio.readline)
    
    variables = []
    for toknum, tokval, _, _, _  in tokens:
        if toknum == token.NAME:
            if (tokval != "exp") and (tokval != "sqrt"):
                variables.append(tokval)
                print(toknum, tokval)

    IP = 1
    EA = 10
    for Z in range(1,10):
        y = eval(code)
        print(y)
