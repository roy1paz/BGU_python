import math
from random import randint

import torch as t
import argparse

from parctical.commons import time_it, read_matrix_from_csv


def my_l2(v: t.tensor) -> float:
    '''
    calculates L2 norm naivly
    :param v: vector to calculate norm of
    :type v: pytorch tensor
    :return: L2 norm of the vector
    :rtype: float
    '''
    sum = 0
    for val in v:
        sum += pow(val, 2)
    res = math.sqrt(sum)
    return res


def my_norm_largest(v: t.tensor) -> float:
    '''
    calculates norm as max value in vector v
    :param v: vector to calculate norm of
    :type v: pytorch tensor
    :return: max value of entry in vector
    :rtype:
    '''
    m = float(t.max(v))
    return m


def my_norm_smallest(v: t.tensor) -> float:
    '''
    calculates norm by returning the smallest entry in the vector
    :param v: vector to norm
    :type v: tensorflow vector
    :return: value of the smallest entry in the vector
    :rtype: float
    '''
    m = float(t.min(v))
    return m


def my_norm_largest_bad(v: t.tensor) -> float:
    '''
    calculates the norm by returning the largest entry in the vector
    should preform poorly due to pytonish implementation
    :param v: vector on which to calculate norm
    :type v: pytorch tensor
    :return: the largest number in the vector
    :rtype: float
    '''
    largest = v[0]
    for val in v:
        largest = max(val, largest)
    return float(largest)


def power_method(M: t.tensor, v: t.tensor, delta: float, norm_func: callable) -> t.tensor:
    '''
    Calculates the eigenvalue of a matrix using the power method
    :param M: Matrix to preform power iteration on
    :type M: pytorch tensor
    :param v: Starting guess of eigenvector
    :type v: pytorch tensor
    :param delta: stop condition
    :type delta: float
    :param norm_func: the normalization function to use
    :type norm_func: callable
    :return: eigenvector
    :rtype: pytorch tensor
    '''
    last_norm = -1
    norm = 0
    iter = 0
    while iter < 2 or abs(norm - last_norm) > delta:
        v = t.matmul(M, v)
        last_norm = norm
        norm = norm_func(v)
        v = v / norm
        iter += 1
    v = t.matmul(M, v)
    norm = norm_func(v)
    return float(norm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, help='path to csv representing matrix to use')
    parser.add_argument('-b', type=str, help='path to csv representing b values to use')
    parser.add_argument('-s', type=int, help='Set random seed to a fixed value', default=randint(0, 1000))
    parser.add_argument('-d', type=float, help='Set the required delta- precision', default=0.0001)
    args = parser.parse_args()

    matrix_path = args.m
    b_path=args.b
    random_seed = args.s
    delta = args.d

    t.manual_seed(random_seed)
    M=read_matrix_from_csv(matrix_path)
    v = read_matrix_from_csv(b_path)

    l2_norm = time_it(power_method, 1, (M, v, delta, t.linalg.norm))
    smallest_norm = time_it(power_method, 2, (M, v, delta, my_norm_smallest))
    largest_norm = time_it(power_method, 3, (M, v, delta, my_norm_largest))
    largest_bad_norm = time_it(power_method, 4, (M, v, delta, my_norm_largest_bad))

    print(f'standart_norm= {l2_norm}\nlargest_norm={largest_norm}\nsmallest_norm={smallest_norm}')
