"""
In this assignment you should find the area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and 
the leftmost intersection points of the two functions. 

The functions for the numeric answers are specified in MOODLE. 


This assignment is more complicated than Assignment1 and Assignment2 because: 
    1. You should work with float32 precision only (in all calculations) and minimize the floating point errors. 
    2. You have the freedom to choose how to calculate the area between the two functions. 
    3. The functions may intersect multiple times. Here is an example: 
        https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx
    4. Some of the functions are hard to integrate accurately. 
       You should explain why in one of the theoretical questions in MOODLE. 

"""

import numpy as np
import time
import random
import copy

class Assignment3:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def integrate(self, f: callable, a: float, b: float, n: int) -> np.float32:
        """
        Integrate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the integration error. 
        Your secondary objective is minimizing the running time. The assignment
        will be tested on variety of different functions. 
        
        Integration error will be measured compared to the actual value of the 
        definite integral. 
        
        Note: It is forbidden to call f more than n times. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the integration range.
        b : float
            end of the integration range.
        n : int
            maximal number of points to use.

        Returns
        -------
        np.float32
            The definite integral of f between a and b
        """

        def collect_points(a,b,n):
            x = 0
            h = (b - a) / (3 * n)
            p_num = 3*n + 1
            points = []
            x = a
            for i in range(p_num):  # split to m parts
                x = a + i*h
                points.append(x)
                # x += step
            return points

        def sum_poly(f,p,n):
            # Wi * f(Xi)+ En || w0 = 1 w1= 3 w2= 3 w3= 1 || En= Cn*h^(n+3)*(f(zeta))**(n+2)| Cn= (-3/80) |replace (n+2),(n+1) for odd
            sum_p1 = 0
            sum_p2 = 0
            for i in range(1,n+1):
                sum_p1 = sum_p1 + f(p[3*i-2]) + f(p[3*i-1])
            for i in range(1,n):
                sum_p2 = sum_p2 + f(p[3 * i])
            total_p = f(p[0]) + (3 * sum_p1) + (2 * sum_p2) + f(p[-1])
            return total_p

        def sp(n,s_p): # m here is n of the function. m parts |||| simpson's method
            m = 3   # simpson's method calls it 'n', rank of the poly in each outer part
            A = 3/8
            h = (b - a) / (m * n)
            simpson = A * h * s_p
            return simpson

        c_points = collect_points(a, b, n)
        s_p = sum_poly(f, c_points, n)
        result = sp(n,s_p)
        return np.float32(result)


    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        """
        Finds the area enclosed between two functions. This method finds
        all intersection points between the two functions to work correctly.

        Example: https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx

        Note, there is no such thing as negative area.

        In order to find the enclosed area the given functions must intersect
        in at least two points. If the functions do not intersect or intersect
        in less than two points this function returns NaN.


        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """
        def find_root(f,a,b,maxerr): # newton-raphson method
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



        def find_roots(f,a,b,maxerr,f1,f2): # durand - kerner method
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

            root_guess = sorted(root_guess)
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

        result = 0
        ass3 = Assignment3()
        a = 1
        b = 100
        maxerr = 0.001
        g = f1 - f2   # new function
        g_tag = np.polyder(g)
        search = True
        if g.o < 2:
            return np.nan
        elif check_Inflection_point(g): # if Inflection point f'n(0) = 0 used the newton-raphson method
            X = find_root(g, a, b, maxerr)
        elif g_tag(0) == 0:     # if f'(0) = 0 used the newton-raphson method, else durand - kerner
            X = find_root(g, a, b, maxerr)
            if X[0] > 0:
                start = a
                while search:
                    r = find_root(g,start,0,maxerr)[0]
                    if np.isnan(r) or [True for i in X if abs(r - i) < 0.01]:
                        search = False
                    else:
                        X.append(r)
                        start = r
            else:
                end = b
                while search:
                    r = find_root(g, 0, end, maxerr)[0]
                    if np.isnan(r) or [True for i in X if abs(r - i) < 0.01]:
                        search = False
                    else:
                        X.append(r)
                        end = r
        else:                               # else durand - kerner
            X = find_roots(g,a,b,maxerr,f1,f2)
        intersection_points = sorted(X)
        if len(intersection_points) < 2:
            return np.nan
        else:
            for i in range(len(intersection_points)-1):
                start = intersection_points[i]
                end = intersection_points[i+1]
                result += ass3.integrate(g,start,end,g.o)

        return np.float32(result)


##########################################################################
#### [a,b] = [1,100]

import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment3(unittest.TestCase):

    def test_integrate_float32(self):
        ass3 = Assignment3()
        f1 = np.poly1d([1, 0, 1])
        r = ass3.integrate(f1, -1, 1, 3)
        print(r)
        self.assertEqual(r.dtype, np.float32)

    def test_integrate_hard_case(self):
        ass3 = Assignment3()
        f1 = strong_oscilations()
        r = ass3.integrate(f1, 0.09, 10, 20)
        true_result = -7.78662 * 10 ** 33
        self.assertGreater(0.001,abs((r - true_result) / true_result))


if __name__ == "__main__":
    unittest.main()
