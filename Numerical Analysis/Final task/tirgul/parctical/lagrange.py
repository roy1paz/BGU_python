import argparse
import csv
import operator
from functools import reduce
import time
import torch as t
from numpy import genfromtxt
import numpy as np
from scipy.interpolate import lagrange

# from tirgul.parctical.output.commons import time_it, multi_time

def time_it(function: callable, ind: int, args: tuple) -> object:
    '''
    times function execution time
    :param function: function to time
    :type function: callable
    :param ind: id of current timeing
    :type ind: int
    :param args: tuple of argument for the function
    :type args: tuple
    :return:
    :rtype: object
    '''
    start = time.time()
    res = function(*args)
    print(f'run of function id {ind} took {time.time() - start}')
    return res


def multi_time(function: callable, ind: int, args: tuple) -> object:
    '''
    calculates execution time of recurring function, calls the output of the last iteration
    :param function: starting function to time, will return other functions
    :type function: callable
    :param ind: id of current timing
    :type ind: int
    :param args: tuple of the length of times to run the sequence
    :type args: tuple of tuples
    :return:
    :rtype: object
    '''
    start = time.time()
    res = function
    for i in range(len(args)):
        res = res(*args[i])
    print(f'run of all function id {ind} took {time.time() - start}')
    return res

def real_func(x: float) -> float:
    '''
    The real function we want to mimic using interpolation
    :param x: x value to calculate
    :type x: float
    :return: the y value where x=x
    :rtype: float
    '''
    return np.sin(x) + np.power(x, 2)


def better_lagrange(x_values: np.ndarray, y_values: np.ndarray) -> callable:
    '''
    more fancy implementation of the lagrange interpolation
    :param x_values: array of x values
    :type x_values: ndarray
    :param y_values: array of y values
    :type y_values: ndarray
    :return: function that receives 1 argument, which is the x value to check
    :rtype: callable
    '''

    def _wrapper(x):  # the polonium of the lagrange interpolation
        def _li(i):  # ech section of the lagrange polonium (Li)
            p = [(x - x_values[j]) / (x_values[i] - x_values[j]) for j in range(k) if j != i]
            return reduce(operator.mul, p)

        k = len(x_values)
        return sum(_li(i) * y_values[i] for i in range(k))

    return _wrapper


def my_lagrange(x: np.ndarray, y: np.ndarray, to_check_x: float) -> float:
    '''
    naive implementation of the lagrange interpolation method
    :param x: array of x values
    :type x: ndarray
    :param y: array of y values
    :type y: ndarray
    :param to_check_x: x value to check what y value is
    :type to_check_x: float
    :return: the y value of the interpolation polonium where x=x
    :rtype: flaot
    '''
    n = len(x)
    sum = 0
    for i in range(n):
        li = 1
        for j in range(n):
            if i != j:
                li = li * (to_check_x - x[j]) / (x[i] - x[j])
        sum = sum + y[i] * li
    return sum

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=float, help='start x value')
    parser.add_argument('-e', type=float, help='end x value')
    parser.add_argument('-d', type=float, help='step of x values', default=1)
    parser.add_argument('-t', type=float, help='target x value')
    args = parser.parse_args()

    x_start = args.s
    x_end = args.e
    step = args.d

    X = np.arange(x_start, x_end, step)
    Y = real_func(X)
    x_test = args.t
    real_y = real_func(x_test)

    res1 = multi_time(lagrange, 1, ((X, Y), (x_test,)))
    res2 = time_it(my_lagrange, 2, (X, Y, x_test))
    res3 = multi_time(better_lagrange, 3, ((X, Y), (x_test,)))
    print(f'{abs(res1 - real_y)}\n{abs(real_y - res2)}\n{abs(real_y - res3)}')
