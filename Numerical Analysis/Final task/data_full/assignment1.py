"""
In this assignment you should interpolate the given function.
"""

import numpy as np
import time
import random
import operator
from functools import reduce
from scipy.misc import derivative

class Assignment1:

    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        starting to interpolate arbitrary functions.
        """
        pass

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Interpolate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the interpolation error.
        Your secondary objective is minimizing the running time. 
        The assignment will be tested on variety of different functions with 
        large n values. 
        
        Interpolation error will be measured as the average absolute error at 
        2*n random points between a and b. See test_with_poly() below. 

        Note: It is forbidden to call f more than n times. 

        Note: This assignment can be solved trivially with running time O(n^2)
        or it can be solved with running time of O(n) with some preprocessing.
        **Accurate O(n) solutions will receive higher grades.** 
        
        Note: sometimes you can get very accurate solutions with only few points, 
        significantly less than n. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        n : int
            maximal number of points to use.

        Returns
        -------
        The interpolating function.
        """

        def chebyshev(g,a, b, n):     # Sample points by using Chebyshev
            x_values, y_values = [], []
            for i in range(n):
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
                return sum([_li(i) * y_values[i] for i in range(k)])
            return _wrapper

        def horner_poly(g):  # O(n)
            def poly(x):
                p = g[0]
                for i in range(1, ):
                    p = p * x + g[i] # call f n-1 times
                return p
            return poly

        g = f
        if type(g) != np.poly1d:    # for non pol
            x_values, y_values = chebyshev(g, a, b, n)  # sample the points
            result = lagrange_interpolation(x_values,y_values) # get the function of the interpolation
        else:
            result = horner_poly(g)  # get the function of the interpolation
        return result


##########################################################################


import unittest
from functionUtils import *
from tqdm import tqdm


class TestAssignment1(unittest.TestCase):

    def test_with_poly(self):
        T = time.time()

        ass1 = Assignment1()
        mean_err = 0

        d = 300
        for i in tqdm(range(100)):
            a = np.random.randn(d)

            f = np.poly1d(a)
            ff = ass1.interpolate(f, -10, 10, 300 + 1)

            xs = np.random.random(200)
            err = 0
            for x in xs:
                yy = ff(x)
                y = f(x)
                err += abs(y - yy)

            err = err / 200
            mean_err += err
        mean_err = mean_err / 100

        T = time.time() - T
        print(T)
        print(mean_err)

    def test_with_poly_restrict(self):
        ass1 = Assignment1()
        a = np.random.randn(5)
        f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
        ff = ass1.interpolate(f, -10, 10, 10)
        xs = np.random.random(20)
        for x in xs:
            yy = ff(x)


if __name__ == "__main__":
    unittest.main()
