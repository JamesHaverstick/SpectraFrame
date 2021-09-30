import numpy as np

def normalize_to_range(array, R):
    """Returns array normalized to range R."""
    array = array - np.min(array) + R[0]
    return array * (R[1] / np.max(array))
