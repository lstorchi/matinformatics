import parser
formula = "sin(x)*x**2"
code = parser.expr(formula).compile()

from math import sin

for x in range(1,10):
    y = eval(code)
    print(y)
