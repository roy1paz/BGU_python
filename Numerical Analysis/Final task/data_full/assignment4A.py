"""
In this assignment you should fit a model function of your choice to data 
that you sample from a given function. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you take an iterative approach and know that 
your iterations may take more than 1-2 seconds break out of any optimization 
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools 
for solving this assignment. 

"""

import numpy as np
import time
import random
import operator
from functools import reduce


class Assignment4A:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def fit(self, f: callable, a: float, b: float, d:int, maxtime: float) -> callable:
        T = time.time()    #delay
        _, time_check = (f(a), time.time() - T)
        if time_check > maxtime:
            return None
        elif  2 < time_check < maxtime:
            maxtime = maxtime - time_check

        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        f : callable. 
            A function which returns an approximate (noisy) Y value given X. 
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int 
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        a function:float->float that fits f between a and b
        """
        def chebyshev(g,a,b,maxtime):     # Sample points by using Chebyshev
            n = maxtime*2
            x_values, y_values = [], []
            for i in range(int(n)):
                c = -np.cos(((2*i+1)*np.pi)/(2*n))    # calculate chebyshev cross
                x_point = 0.5*(c*(b-a)+(a+b))      # calculate calibration
                y_point = g(x_point)
                x_values.append(x_point)
                y_values.append(y_point)
            return np.array(x_values),np.array(y_values)

        def lagrange_interpolation(x_values: np.ndarray, y_values: np.ndarray) -> callable: # Lagrange interpolation O(n^2)
            def _wrapper(x):  # the polonium of the lagrange interpolation
                def _li(i):  # each section of the lagrange polonium (Li)
                    p = [(x - x_values[j]) / (x_values[i] - x_values[j]) for j in range(k) if j != i]
                    return reduce(operator.mul, p)

                k = len(x_values)
                return sum(_li(i) * y_values[i] for i in range(k))
            return _wrapper

        def horner_poly(g):  # O(n)
            def poly(x):
                p = g[0]
                for i in range(1, ):
                    p = p * x + g[i] # call f n-1 times
                return p
                return poly


        if type(f) != np.poly1d:    # for non pol
            x_values, y_values = chebyshev(f, a, b,maxtime)  # sample the points
            result = lagrange_interpolation(x_values,y_values) # get the function of the interpolation
        else:
            result = horner_poly(g)  # get the function of the interpolation

        return result


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment4(unittest.TestCase):

    def test_return(self):
        f = NOISY(0.01)(poly(1,1,1))
        ass4 = Assignment4A()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertLessEqual(T, 5)

    def test_delay(self):
        f = DELAYED(7)(NOISY(0.01)(poly(1,1,1)))

        ass4 = Assignment4A()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertGreaterEqual(T, 5)

    def test_err(self):
        f = poly(1,1,1)
        nf = NOISY(1)(f)
        ass4 = Assignment4A()
        T = time.time()
        ff = ass4.fit(f=nf, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        mse=0
        for x in np.linspace(0,1,1000):
            self.assertNotEqual(f(x), nf(x))
            mse+= (f(x)-ff(x))**2
        mse = mse/1000
        print(mse)


if __name__ == "__main__":
    unittest.main()
