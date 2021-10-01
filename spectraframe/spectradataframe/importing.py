"""
Define functions to import .csv or .tsv files.
"""
import pandas as pd
from .spectradataframe import SpectraDataFrame


def read_csv(path, sep=None, header=None):
    if sep is None:
        sep = ','
    if header is None:
        header = 'infer'
    df = pd.read_csv(path, sep=sep, header=header)
    return SpectraDataFrame(df)


def read_tsv(path, sep=None, header=None):
    if sep is None:
        sep = '\t'
    if header is None:
        header = 'infer'
    df = pd.read_csv(path, sep=sep, header=header)
    return SpectraDataFrame(df)