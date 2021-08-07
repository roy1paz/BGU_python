"""
In this assignment you should fit a model function of your choice to data 
that you sample from a contour of given shape. Then you should calculate
the area of that shape. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you know that your iterations may take more 
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment. 
Note: !!!Despite previous note, using reflection to check for the parameters 
of the sampled function is considered cheating!!! You are only allowed to 
get (x,y) points from the given shape by calling sample(). 
"""
import numpy as np
import time
import random
from operator import itemgetter
from functionUtils import AbstractShape
import operator
from functools import reduce


class MyShape(AbstractShape):
    # change this class with anything you need to implement the shape
    def __init__(self):
        pass


class Assignment4:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def area(self, contour: callable, maxerr=0.001)->np.float32:
        """
        Compute the area of the shape with the given contour. 

        Parameters
        ----------
        contour : callable
            Same as AbstractShape.contour 
        maxerr : TYPE, optional
            The target error of the area computation. The default is 0.001.

        Returns
        -------
        The area of the shape.

        """

        def collect_points(contour):  # takes 10000 samples [[a.],....,[a.]]
            points = contour(10000)
            return points

        def trapezoidal_rule(p):
            area = 0
            j = len(p) - 1
            for i in range(len(p)):
                area += (p[j][0] + p[i][0]) * (p[j][1] - p[i][1])
                j = i  # j is previous vertex to i

            # Return absolute value
            return abs(area / 2.0)

        c_points = collect_points(contour)
        trapezoidal_area = trapezoidal_rule(c_points)
        result = trapezoidal_area
        return np.float32(result)


    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        sample : callable.
            An iterable which returns a data point that is near the shape contour.
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        An object extending AbstractShape.
        """
        T = time.time()

        def generate_points(t, points):  # samples [[a.],....,[a.]]
            values = []
            while time.time() - t < maxtime - 2.5:
                point = points()
                values.append(point)
            sorted_values = sorted(values, key=itemgetter(0))
            x,y = np.float32([i[0] for i in sorted_values]),np.float32([i[1] for i in sorted_values])
            return x,y

        def center_calculate(x_values,y_values):
            center_x,center_y = sum(x_values)/len(x_values), sum(y_values)/len(y_values)
            return center_x,center_y

        def radius_calculate(c_x, c_y, x, y):
            r = []
            for i in range(len(x)):
                r.append(((x[i]-c_x)**2 + (y[i]-c_y)**2)**(0.5))
            r = np.mean(r)
            return r

        class Shape(AbstractShape):
            def __init__(self, cx: np.float32, cy: np.float32,radius: np.float32,x_values,y_values):
                self._radius = radius
                self._cx = cx
                self._cy = cy
                self.x_values = x_values
                self.y_values = y_values
            def sample(self):
                w = np.random.random() * 2 * np.pi
                x = np.cos(w) * self._radius + self._cx
                y = np.sin(w) * self._radius + self._cy
                return x, y

            def contour(self, n: int):
                w = np.linspace(0, 2 * np.pi, num=n)
                x = np.cos(w) * self._radius + self._cx
                y = np.sin(w) * self._radius + self._cy
                xy = np.stack((x, y), axis=1)
                return xy

            def area(self):
                a = np.pi * self._radius ** 2
                return a

        x_values,y_values = generate_points(T,sample)
        center_x,center_y = center_calculate(x_values, y_values)
        radius = radius_calculate(center_x,center_y,x_values,y_values)
        result = Shape(center_x,center_y,radius,x_values,y_values)
        if time.time() - T < maxtime:
            time.sleep(round(maxtime - (time.time() - T)))


        return result


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment4(unittest.TestCase):

    def test_return(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit_shape(sample=circ, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertLessEqual(T, 5)

    def test_delay(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)

        def sample():
            time.sleep(1)
            return circ()

        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit_shape(sample=sample, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertGreaterEqual(T, 5)

    def test_circle_area(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)

    def test_bezier_fit(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit_shape(sample=circ, maxtime=5)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)

    def test_circle_area_from_contour(self):
        circ = Circle(cx=1, cy=1, radius=1, noise=0.0)
        ass4 = Assignment4()
        T = time.time()
        a_computed = ass4.area(contour=circ.contour, maxerr=0.1)
        T = time.time() - T
        a_true = circ.area()
        self.assertLess(abs((a_true - a_computed)/a_true), 0.1)


if __name__ == "__main__":
    unittest.main()
