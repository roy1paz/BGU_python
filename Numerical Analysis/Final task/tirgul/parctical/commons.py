import csv
import time
import torch as t
from numpy import genfromtxt

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


def save_matrix_as_csv(path, m):
    '''
    saves a matrix to csv
    :param path: path in which the csv will be saved
    :type path: str
    :param m: matrix to save
    :type m: pytorch tensor
    :return: nothing
    :rtype: None
    '''
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        for row in m:
            float_row=list(map(lambda x:float(x),row))
            w.writerow(float_row)

def read_matrix_from_csv(path):
    '''
    reads a csv file and return the matrix it represents
    :param path: path to the csv file
    :type path: string
    :return: matrix
    :rtype: pytorch tensor
    '''
    data=genfromtxt(path,delimiter=',')
    tens=t.as_tensor(data)
    return tens

if __name__ =='__main__':
    size=100
    for i in range(5):
        m=t.rand(size,size)
        save_matrix_as_csv(rf'C:\Users\Lior\Desktop\אנליזה נומרית\parctical\matricies\m_{i}.csv',m)