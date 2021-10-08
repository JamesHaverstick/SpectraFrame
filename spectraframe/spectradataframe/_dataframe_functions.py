import numpy as np

def normalize_to_range(array, R):
    """Returns array normalized to range R."""
    array = array - np.min(array) + R[0]
    return array * (R[1] / np.max(array))


def bound_errors(x, x1, x2):
    if x1 >= x2:
        raise ValueError('x2 must be greater than x1')
    if x1 >= x[-1]:
        raise ValueError('x1 is out of range.')
    if x2 <= x[0]:
        raise ValueError('x2 is out of range')
