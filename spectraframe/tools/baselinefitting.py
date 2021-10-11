import pandas as pd
from scipy.optimize import curve_fit
from ..spectradataframe.spectradataframe import SpectraDataFrame
import numpy as np


def fit_baseline(sdf, func, regions=None, p0=None, bounds=(-np.inf, np.inf)):
    baseline_data = {sdf.xname: sdf.x}
    corrected_data = {sdf.xname: sdf.x}
    params = {}
    sdfcopy = sdf.copy()
    if regions is not None:
        sdfcopy.crop(regions[0][0], regions[-1][1])
        if len(regions) == 1:
            pass
        else:
            for i in range(len(regions) - 1):
                sdfcopy.remove_region(regions[i][1], regions[i+1][0])
    for name in sdf.names:
        popt, pcov = curve_fit(func,
                               sdfcopy.x,
                               sdfcopy[name],
                               bounds=bounds,
                               p0=p0)
        baseline_data[name] = np.array([func(i, *popt) for i in sdf.x])
        corrected_data[name] = sdf[name] - baseline_data[name]
        params[name] = popt
    return SpectraDataFrame(pd.DataFrame(corrected_data)), \
           SpectraDataFrame(pd.DataFrame(baseline_data)), params
