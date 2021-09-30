import pandas as pd
import numpy as np
from scipy import integrate
from dataframe_functions import normalize_to_range


class SpectraDataFrame:
    def __init__(self,
                 df: pd.DataFrame,
                 xname=None):
        if xname is None:
            self.xname = df.columns[0]
        else:
            self.xname = xname
        self.df = df
        self.x = None
        self._update()

    def __getitem__(self, key):
        """Return series of column with given column name."""
        return self.df[key]

    def __contains__(self, item):
        return item in self.specnames()

    def _update(self):  # after changing some aspect of df
        self.x = np.array(self.df[self.xname])

        if self.x[0] > self.x[1]:  # if x axis is decreasing
            self.df = self.df.iloc[::-1]  # reverse order
            self.x = np.array(self.df[self.xname])  # reset self.x

    def crop(self, x1, x2):
        self.df = self.df[self.df[self.xname] < x2]
        self.df = self.df[self.df[self.xname] > x1]
        self._update()

    def spectra(self):
        """Returns DataFrame with x-axis dropped."""
        return self.df.drop([self.xname], axis=1)

    def specnames(self):
        """Returns names of spectra (column names)"""
        return self.spectra().columns

    def mean(self):
        """Returns average spectrum."""
        return np.array(self.spectra().mean(axis=1))

    def std(self):
        """Returns standard deviation at each measurement point."""
        return np.array(self.spectra().std(axis=1))

    def sem(self):
        """Return standard error at each measurement point."""
        return np.array(self.spectra().sem(axis=1))

    def normalize_by_area(self, zero=True, area=None):
        """Normalizes all spectra to the same area."""
        if area is None:
            area = 1
        for col in self.specnames():
            spectra = np.array(self.df[col])
            if zero:
                spectra = spectra - np.min(spectra)
            self.df[col] = area * spectra * \
                (1 / integrate.cumtrapz(spectra, self.x, initial=0)[-1])

    def normalize(self, value_range=None):
        """Normalizes spectra between two values. (default: 0,1)"""
        if value_range is None:
            value_range = (0, 1)
        else:
            if value_range[0] > value_range[1]:
                raise ValueError('The first element of value_range should be less than the second element.')
        for col in self.specnames():
            self.df[col] = normalize_to_range(self.df[col], value_range)
