import numpy 
import pandas

from snn import *

if __name__ == "__main__":

    x = numpy.array([[0,0,1],
                     [0,1,1],
                     [1,0,1],
                     [1,1,1]])
    y = numpy.array([[0],[1],[1],[0]])

    nn = simplenn(x,y)

    for i in range(1500):
        nn.feedforward()
        nn.backprop()

    nx = numpy.array([[0,0,1]])
    print("Insert ", nx, " should be 0 ")
    nn.set_pred_input (nx)
    nn.feedforward()
    print(nn.get_output())

    nx = numpy.array([[1,0,1]])
    print("Insert ", nx, " should be 1 ")
    nn.set_pred_input (nx)
    nn.feedforward()
    print(nn.get_output())
