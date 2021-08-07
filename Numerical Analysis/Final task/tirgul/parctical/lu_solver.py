import argparse

import torch as t

from parctical.commons import save_matrix_as_csv, read_matrix_from_csv


def decompose(M: t.tensor) -> (t.tensor, t.tensor):
    '''
    calculates the decomposition of matrix M without needing to use pivot
    :param M: matrix to decompose
    :type M: pytorch matrix
    :return: (L,U) where L is a lower triangular matrix, and U is an upper triangular matrix
    :rtype: tuple of pytorch tensor
    '''
    pass


def solution_finder_given_LU(L: t.tensor, U: t.tensor, b: t.tensor) -> t.tensor:
    '''
    Solves a system of linear equations using given decomposition
    :param L: lower triangular matrix
    :type L: pytorch tensor
    :param U: upper triangular matrix
    :type U: pytorch tensor
    :param b: vector of free variables
    :type b: pytorch tensor
    :return: vector of solution X s.t LUX=b
    :rtype: pytorch tensor
    '''
    pass


def solution_finder(M: t.tensor, b: t.tensor) -> t.tensor:
    '''
    Solves a system of linear equations using LU decomposition
    :param M: Matrix represents coefficients of the variables
    :type M: pytorch tensor
    :param b: vector of free variables
    :type b: pytorch tensor
    :return: vector of solution X s.t MX=b
    :rtype: pytorch tensor
    '''
    L, U = decompose(M)
    return solution_finder_given_LU(L, U, b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, help='path sv file representing matrix to solve')
    parser.add_argument('-b', type=str, help='path to csv file representing b values')
    parser.add_argument('-o', type=str, help='output path')

    args = parser.parse_args()

    matrix_path = args.m
    b_path = args.b
    output_path = args.o

    M = read_matrix_from_csv(matrix_path)
    b = read_matrix_from_csv(b_path)

    sol = solution_finder(M, b)
    save_matrix_as_csv(output_path, sol)
