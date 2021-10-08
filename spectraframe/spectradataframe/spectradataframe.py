"""
Define SpectraDataFrame class
"""
import pandas as pd
import numpy as np
from scipy import integrate
from typing import Union
from ._dataframe_functions import normalize_to_range, bound_errors


class SpectraDataFrame:
    def __init__(self,
                 data: Union[pd.DataFrame, dict],
                 xname=None):
        """
        Returns Constructs SpectraDataFrame
        :param data: pandas DataFrame or dict
        :param xname: name of column or key containing x-values. By default this is the first column.
        """
        if type(data) is dict:  # Make sure data is a DataFrame
            data = pd.DataFrame(data)
        if xname is None:
            self.xname = data.columns[0]
        else:
            self.xname = xname
        self.df = data
        self._index = -1
        self.x = None
        self.names = None
        self._are_ints_in_names = False
        self._update()

    def __iter__(self):
        return iter(self.names)

    def __getitem__(self, key):
        """Return series of column with given column name or index."""
        if type(key) is int:
            if self._are_ints_in_names:
                try:
                    return self.df[key]
                except KeyError:
                    raise KeyError(f'{key} not found. Selecting by index is\
                     disabled when spectra have integer names')
            else:
                return self.df[self.names[key]]
        else:
            return self.df[key]

    def __setitem__(self, key, value):
        """Adds or changes spectra"""
        if key == self.xname:
            raise KeyError('Key is name of x-axis. Cannot change contents of x-axis this way.')
        else:
            self.df[key] = value
            self._update()

    def __contains__(self, item):
        """Checks if item is a name of any spectra column."""
        return item in self.names

    def _update(self):
        """Update attributes after changing some aspect of self.df."""
        self.x = np.array(self.df[self.xname])

        if self.x[0] > self.x[1]:  # if x axis is decreasing
            self.df = self.df.iloc[::-1]  # reverse order
        self.x = np.array(self.df[self.xname])  # reset self.x
        self.names = self.spectra().columns
        self._are_ints_in_names = False
        for name in self.names:
            if type(name) == int:
                self._are_ints_in_names = True
                break

    def to_csv(self, path, sep=None, header=True):
        """
        Save data as a text file.
        :param path: Path to save data.
        :param sep: Separator to use. (Default ',')
        :param header: Whether to include column names.
        :return: None
        """
        if sep is None:
            sep = ','
        self.df.to_csv(path, sep=sep, header=header, index=False)

    def to_tsv(self, path, sep=None, header=True):
        """
        Save data as a text file.
        :param path: Path to save data.
        :param sep: Separator to use. (Default '\t')
        :param header: Whether to include column names.
        :return: None
        """
        if sep is None:
            sep = '\t'
        self.df.to_csv(path, sep=sep, header=header, index=False)

    def copy(self):
        """Return a copy of SpectraDataFrame object."""
        return SpectraDataFrame(self.df.copy(deep=True))

    def remove(self, names):
        """
        Remove spectra in place.
        :param names: List of column names to remove.
        :return: None
        """
        self.df = self.df.drop(names, axis=1)
        self._update()

    def drop(self, names):
        """
        Returns a SpectraDataFrame with removed columns.
        :param names: List of column names to remove.
        :return: SpectraDataFrame
        """
        return SpectraDataFrame(self.df.drop(names, axis=1))

    def apply_function(self, func, inplace=True):
        """
        Applies a function to all spectra.
        function arguments:
            numpy array with x-values.
            pandas series with spectra values.
        function returns:
            array-like replacement spectra, should be same length as input
        """
        new_df = pd.DataFrame(data={self.xname: self.x})
        for col in self.names:
            new_df[col] = func(self.x, self[col])
        if inplace:
            self.df = new_df
            self._update()
        else:
            return SpectraDataFrame(new_df)

    def crop(self, x1, x2, inplace=True):
        """
        Crops data to range [x1,x2]. (Inclusive range)
        :param x1: x-value for lower bound.
        :param x2: x-value for upper bound.
        :param inplace: Perform operation in-place or return a new instance.
        :return: None or SpectraDataFrame
        """
        bound_errors(self.x, x1, x2)
        if inplace:
            self.df = self.df[self.df[self.xname] <= x2]
            self.df = self.df[self.df[self.xname] >= x1]
            self._update()
        else:
            new_df = self.df[self.df[self.xname] <= x2]
            new_df = new_df[new_df[self.xname] >= x1]
            return SpectraDataFrame(new_df)

    def remove_region(self, x1, x2, inplace=True):
        bound_errors(self.x, x1, x2)
        if inplace:
            self.df = self.df[self.df[self.xname] <= x1 or self.df[self.xname] >= x2]
            self._update()
        else:
            new_df = self.df[self.df[self.xname] <= x1 or self.df[self.xname] >= x2]
            return SpectraDataFrame(new_df)

    def spectra(self):
        """Returns DataFrame with x-axis dropped."""
        return self.df.drop([self.xname], axis=1)

    def mean(self):
        """Returns average spectrum."""
        return np.array(self.spectra().mean(axis=1))

    def std(self):
        """Returns standard deviation at each measurement point."""
        return np.array(self.spectra().std(axis=1))

    def sem(self):
        """Return standard error at each measurement point."""
        return np.array(self.spectra().sem(axis=1))

    def normalize(self, method='default', params=None):
        """
        Normalize the spectra by various methods.
        :param method: str of method to use
        :param params: various params to apply
        :return: None
        """
        if params is None:
            params = {}
        if method in ['default', 'Default']:
            value_range = params['range'] if 'range' in params else (0, 1)
            if value_range[0] > value_range[1]:
                raise ValueError('The first element of value_range should be less than the second element.')
            for col in self.names:
                self.df[col] = normalize_to_range(self.df[col], value_range)
        elif method in ['area', 'Area']:
            area = params['area'] if 'area' in params else 1
            zero = params['zero'] if 'zero' in params else True
            for col in self.names:
                spectra = np.array(self.df[col])
                if zero:
                    spectra = spectra - np.min(spectra)
                self.df[col] = area * spectra * \
                    (1 / integrate.cumtrapz(spectra, self.x, initial=0)[-1])
        elif method in ['mean', 'Mean',
                        'average', 'Average']:
            mean = params['mean'] if 'mean' in params else 1
            zero = params['zero'] if 'zero' in params else True
            for col in self.names:
                spectra = np.array(self.df[col])
                if zero:
                    spectra = spectra - np.min(spectra)
                self.df[col] = spectra * (mean / np.mean(spectra))


