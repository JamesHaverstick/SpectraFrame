import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from ..spectradataframe.spectradataframe import SpectraDataFrame


def interpolate(sdf: SpectraDataFrame, new_x):
    """
    Returns a SpectraDataFrame with new_x values and spectra linearly interpolated to new_x values.
    :param sdf: SpectraDataFrame to interpolate.
    :param new_x: x values to interpolate to.
    :return: SpectraDataFrame with interpolated y values.
    """
    data = {sdf.xname: new_x}
    for col in sdf.names:
        func = interp1d(sdf.x, sdf[col])
        data[col] = np.fromiter(map(func, new_x), float)
    return SpectraDataFrame(pd.DataFrame(data))
