from distutils.core import setup


setup(
    name='spectraframe',
    version='0.2.0',
    packages=['spectraframe',
              'spectraframe.spectradataframe',
              'spectraframe.plotting',
              'spectraframe.tools'],
    license='MIT License',
    description='Package to work with sets of spectroscopic data in python.',
    author='James Haverstick',
    author_email='jhaverstick99@gmail.com'
)
