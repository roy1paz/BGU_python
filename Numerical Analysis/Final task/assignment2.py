"""
In this assignment you should find the intersection points for two functions.
"""

import numpy as np
import time
import random
import copy


class Assignment2:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> callable:
        """
        Find as many intersection points as you can. The assignment will be
        tested on functions that have at least two intersection points, one
        with a positive x and one with a negative x.


        Parameters
        ----------
        f1 : callable
            the first given function
        f2 : callable
            the second given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        maxerr : float
            An upper bound on the difference between the
            function values at the approximate intersection points.


        Returns
        -------
        X : iterable of approximate intersection Xs such that for each x in X:
            |f1(x)-f2(x)|<=maxerr.

        """

        def find_root(f,a,b,maxerr): # newton method
            roots = []
            k = f.o  # rank
            f_derivative = f.deriv()
            x_old = (a+b)/2
            if f_derivative(x_old) == 0:
                x_old = 0.001
            search = True
            T = time.time()
            while search:
                if (time.time() - T) > 10:
                    return np.nan
                if f_derivative(x_old) == 0:  # formula for case f'(0) = 0
                    x_new = x_old - ((x_old**k)/(k*(x_old **(k-1))))
                else:
                    x_new = x_old - (f(x_old)) / (f_derivative(x_old)) # x_nt = X_n - f(x_n)/f'(x_n)
                if abs(f(x_new) - f(x_old)) < maxerr:
                    roots.append(x_new)
                    search = False
                else:
                    x_old = x_new
            return roots


        def find_roots(f,a,b,maxerr,f1,f2): # durand - kerner
            root_guess = [] #start roots
            n = f.o  # rank
            c = np.pi/(2*n)
            teta = (2*np.pi)/n
            r = abs(a/b) ** (1/n) #radius
            for k in range(n):
                guess = r * np.exp(1J*(k*teta+c)) # Euler's formula
                root_guess.append(guess)
            search = True
            while search:
                old_roots = copy.deepcopy(root_guess)
                for i in range(len(root_guess)):
                    roots_sum = extra(i,old_roots)
                    root_guess[i] = old_roots[i] - (f(old_roots[i]) / roots_sum) # x_nt = X_n - f(x_n)/f'(x_n)
                search = error(root_guess,old_roots,maxerr,n,f1,f2)
            return root_guess


        def extra(i, old_roots):
            sum = 1
            for index in range(len(old_roots)):
                if i != index:
                    sum = sum * (old_roots[i] - old_roots[index])  # (rn-sn)(rn-tn)...
            return sum


        def error(root_guess, old_roots, maxerr, n, f1, f2):
            count = 0
            search = True
            for root, i in zip(root_guess, range(len(root_guess))):
                err = abs(root_guess[i] - old_roots[i])
                err2 = abs(f1(root) - f2(root))
                if err < maxerr and err2 < maxerr:  # check if the roots are found
                    count += 1
                    if count == n:
                        search = False
                else:
                    count = 0
            return search

        def falsePosition(x0, x1,e,f):
            step = 1
            max_iter = 0
            condition = True
            while condition:
                max_iter += 1
                x2 = x0 - (x1 - x0) * f(x0) / (f(x1) - f(x0))
                if f(x0) * f(x2) < 0:
                    x1 = x2
                else:
                    x0 = x2
                step = step + 1
                condition = abs(f(x2)) > e
            return x2


        def check_Inflection_point(f_check): # check Inflection point on g func
            if f_check.o % 2 == 0:
                n_div = f_check.o
            else:
                n_div = f_check.o - 1
            for i in range(n_div):
                f_check = np.polyder(f_check)
            if f_check(0) == 0:
                return True
            else:
                return False


        g = f1 - f2   # new function
        g_tag = np.polyder(g)
        search = True
        if g.o == 0:
            return None
        if check_Inflection_point(g): # if Inflection point f'n(0) = 0 used the newton-raphson method
            X = find_root(g, a, b, maxerr)
        elif g_tag(0) == 0:     # if f'(0) = 0 used the newton-raphson method, else durand - kerner
            X = find_root(g, a, b, maxerr)
            if X[0] > 0:
                start = a
                while search:
                    r = find_root(g,start,0,maxerr)[0]
                    if np.isnan(r) or [True for i in X if abs(r - i) < maxerr]:
                        return X
                    else:
                        X.append(r)
                        start = r
            else:
                end = b
                while search:
                    r = find_root(g, 0, end, maxerr)[0]
                    if np.isnan(r) or [True for i in X if abs(r - i) < maxerr]:
                        return X
                    else:
                        X.append(r)
                        end = r
        else:                               # else durand - kerner
            X = find_roots(g,a,b,maxerr,f1,f2)
        return X


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment2(unittest.TestCase):

    def test_sqr(self):

        ass2 = Assignment2()

        f1 = np.poly1d([-1,0,1])
        f2 = np.poly1d([1,0,-1])
        X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

    def test_poly(self):

        ass2 = Assignment2()

        f1, f2 = randomIntersectingPolynomials(10)
        X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))


if __name__ == "__main__":
    unittest.main()
