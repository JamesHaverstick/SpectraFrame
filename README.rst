===========
Spectra Frame
===========

Spectra Frame is an under-construction package to make processing
large sets of spectroscopic data easier. It is built on the Pandas library which
makes it extremely flexible. If there is anything that can't be done in Spectra Frame,
then you can get your data as a DataFrame object and program it yourself.
Typical usage looks like this::

    #!/usr/bin/env python

    import spectraframe as sf

    spectra = sf.read_csv(path)

    spectra.crop(400, 2500)

    sf.plot(spectra, with_average=True)



This package is still under development. Here are some other python packages that also focus
on working with spectroscopic data.
If you need a package for python 2 that supports more advanced plotting, check
out Scikitspectra. There is also specutils which is designed for astronomical spectroscopic data.