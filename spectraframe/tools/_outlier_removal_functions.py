import numpy as np


def distance(a, b):
    """
    Return distance between two arrays.
    :param a: array 1
    :param b: array 2
    :return: distance between two arrays.
    """
    return np.sqrt(np.sum(np.square(a - b)))
