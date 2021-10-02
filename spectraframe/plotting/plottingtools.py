"""
Define simple tools to plot SpectraDataFrame objects.
"""
import matplotlib.pyplot as plt
from ..spectradataframe.spectradataframe import SpectraDataFrame


def plot(sdf: SpectraDataFrame,
         x_label=None,
         y_label=None,
         title=None,
         dpi=None,
         linewidth=None,
         plot_average=False):
    """
    Simple function to plot the contents of a SpectraDataFrame with Matplotlib.
    :param sdf: SpectraDataFrame
    :param x_label: label for x-axis.
    :param y_label: label for y-axis.
    :param title: title.
    :param dpi: dpi of plot. (Default 150)
    :param linewidth: linewidth for plot. (Default 0.5)
    :param plot_average: Whether to plot the average value over all spectra.
    :return:
    """
    if dpi is None:
        dpi=150
    if linewidth is None:
        linewidth = 0.5
    plt.figure(dpi=dpi)
    ax = plt.subplot()
    x = sdf.x
    spectra = sdf.spectra()
    for col in sdf.names:
        ax.plot(x, spectra[col], lw=linewidth, label='')
    if plot_average:
        ax.plot(x, sdf.mean(), lw=1, color='red', zorder=200, label='Avg')
        ax.legend()
    if title is not None:
        ax.set_title(title)
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    plt.show()