import numpy 
import pandas

# starting from 
# https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6

def sigmoid(x):
    return 1.0/(1+ numpy.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)

class simplenn:
    def __init__(self, x, y):
        self.__input__    = x
        self.__weights1__ = numpy.random.rand(self.__input__.shape[1],4) 
        self.__weights2__ = numpy.random.rand(4,1)                 
        self.__y__        = y
        self.__output__   = numpy.zeros(self.__y__.shape)

    def get_output(self):
        return self.__output__

    def set_pred_input (self, x):
        self.__input__ = x

    def feedforward(self):
        self.__layer1__ = sigmoid(numpy.dot(self.__input__, self.__weights1__))
        self.__output__ = sigmoid(numpy.dot(self.__layer1__, self.__weights2__))

    def backprop(self):
        d_weights2 = numpy.dot(self.__layer1__.T, \
                (2*(self.__y__ - self.__output__) * \
                sigmoid_derivative(self.__output__)))
        d_weights1 = numpy.dot(self.__input__.T,  \
                (numpy.dot(2*(self.__y__ - self.__output__) * \
                sigmoid_derivative(self.__output__), \
                self.__weights2__.T) * sigmoid_derivative(self.__layer1__)))

        self.__weights1__ += d_weights1
        self.__weights2__ += d_weights2


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
