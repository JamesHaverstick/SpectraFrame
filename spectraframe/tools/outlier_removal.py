import numpy as np
from ._outlier_removal_functions import distance


def pick_outliers(sdf, N, region=None):
    """
    Return N outliers sorted by distance to avg over given region.
    :param sdf: SpectraDataFrame
    :param N: Number of outliers to return
    :param region: Region to confine measurement.
    :return:
    """
    new_sdf = sdf.copy()
    if region is not None:
        new_sdf.crop(region[0], region[1])
    avg = new_sdf.mean()
    distances = [distance(avg, np.array(new_sdf[i])) for i in new_sdf]
    sortedspectra = [x for _, x in sorted(zip(distances, sdf.names))]
    sortedspectra.reverse()
    return sortedspectra[:N]