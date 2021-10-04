import numpy as np

def distance(a, b):
    """
    Return distance between two arrays.
    :param a: array 1
    :param b: array 2
    :return: distance between two arrays.
    """
    return np.sqrt(np.sum(np.square(a - b)))


def pick_outliers(sdf, N, region=None, method='max'):
    """
    Return N outliers sorted by distance to avg over given region.
    :param sdf: SpectraDataFrame
    :param N: Number of outliers to return
    :param region: Region to confine measurement.
    :param method: Method to choose outliers by.
    :return:
    """
    new_sdf = sdf.copy()
    if region is not None:
        new_sdf.crop(region[0], region[1])
    avg = new_sdf.mean()
    if method == 'distance':
        values = [distance(avg, np.array(new_sdf[i])) for i in new_sdf]
    elif method == 'max':
        values = [max(np.abs(avg - np.array(new_sdf[i]))) for i in new_sdf]
    else:
        raise ValueError('Unknown method.')
    sortedspectra = [x for _, x in sorted(zip(values, sdf.names))]
    sortedspectra.reverse()
    return sortedspectra[:N]
