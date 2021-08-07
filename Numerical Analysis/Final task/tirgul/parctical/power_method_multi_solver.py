import argparse
import csv

from parctical.commons import read_matrix_from_csv
from parctical.power_method import power_method
from os import listdir, path
import torch as t


def find_csv_filenames(path_to_dir, suffix=".csv"):
    '''
    lists all the files with suffix in given dir
    :param path_to_dir: directory in which to search files
    :type path_to_dir: string
    :param suffix: csv
    :type suffix: csv
    :return: list of all csv files
    :rtype: list of strings
    '''
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def file_names_to_matrices(file_names,path_to_dir):
    '''
    Reads all csv files of matricies and returns list of tensor objects
    :param file_names: list of csv file names
    :type file_names: list of strings
    :param path_to_dir: path to the directory in which all the csv files are
    :type path_to_dir: string
    :return: list of matrices
    :rtype: list of pytorch tensors
    '''
    res = []
    for f in file_names:
        complete_path= path.join(path_to_dir,f)
        res.append(read_matrix_from_csv(complete_path))
    return res


def get_result_vector(matrices, v, delta, norm):
    '''
    calculates the larges eugenvalue of all each matrix
    :param matrices: list of matrices
    :type matrices: list of pytorch tensors
    :param v: initial guess vector
    :type v: pytorch tensor
    :param delta: acceptable error
    :type delta: float
    :param norm: function to normalize the vector
    :type norm: callable
    :return: list of highest eigenvalues where result[i] is the highest eigenvalue of matrices[i]
    :rtype: list of floats
    '''
    results = []
    for m in matrices:
        res = power_method(m, v, delta, norm)
        results.append(res)
    return results


def save_results_to_csv(results, matrices, output_path):
    with open(output_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['matrix_name', 'largest_ev'])
        for i in range(len(results)):
            w.writerow([matrices[i], results[i]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, help='path to directory where matrices with need to find EV exist')
    parser.add_argument('-b', type=str, help='path to csv representing b values to use')
    parser.add_argument('-d', type=float, help='Set the required delta- precision', default=0.0001)
    parser.add_argument('-o', type=str, help='output path')

    args = parser.parse_args()

    matrix_path = args.c
    b_path = args.b
    delta = args.d
    output_path = args.o
    b=read_matrix_from_csv(b_path)

    norm = t.linalg.norm

    csv_names = find_csv_filenames(matrix_path)
    metricies = file_names_to_matrices(csv_names,matrix_path)
    results=get_result_vector(metricies,b,delta,norm)
    save_results_to_csv(results,csv_names,output_path)
